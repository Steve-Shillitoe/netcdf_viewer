from django.shortcuts import render
from .forms import NetCDFUploadForm
from .models import NetCDFFile
from netCDF4 import Dataset
import plotly.graph_objects as go

def upload_netcdf(request):
    """
    Handle NetCDF file upload and visualization.

    Users can:
    - Upload a NetCDF file
    - Choose a variable to display
    - Choose a time step (if the file has a time axis)
    - See a 2D heatmap of that variable at that time
    """

    # --------------------------------------------------------------------------
    # 'context' is a dictionary that we send to the template.
    # Keys = variable names in the template
    # Values = data/objects we want to display
    # In the template, use {{ key }} to display the value
    # --------------------------------------------------------------------------
    context = {
        "variables": None,          # list of variables in the NetCDF file that can be plotted
        "selected_var": None,       # the variable currently selected by the user
        "times": None,              # array of time points in the NetCDF file
        "selected_time_idx": None,  # the time index selected by the user
        "metadata": None,           # information about dimensions and variables
        "plot_html": None,          # the HTML string for the Plotly heatmap
        "nc_file_instance": None,   # reference to the saved NetCDFFile database record
    }

    # --------------------------------------------------------------------------
    # Check if the form has been submitted
    # --------------------------------------------------------------------------
    if request.method == "POST":
        form = NetCDFUploadForm(request.POST, request.FILES)

        # Check if the form is valid and a file has been uploaded
        if form.is_valid() and 'file' in request.FILES:
            
            # ------------------------------------------------------------------
            # Save uploaded file to the database via the NetCDFFile model.
            # ------------------------------------------------------------------
            nc_file_instance = NetCDFFile.objects.create(file=request.FILES['file'])
            context["nc_file_instance"] = nc_file_instance

            # Full path to the saved file
            nc_path = nc_file_instance.file.path

            # ------------------------------------------------------------------
            # Open the NetCDF file using netCDF4
            # ------------------------------------------------------------------
            ds = Dataset(nc_path, "r")

            # ------------------------------------------------------------------
            # Extract variables with >= 2 dimensions (plottable in 2D)
            # ------------------------------------------------------------------
            variables = [v for v in ds.variables.keys() if len(ds.variables[v].dimensions) >= 2]
            context["variables"] = variables

            # ------------------------------------------------------------------
            # Determine which variable to display
            # If user selected a variable in the form, use that.
            # Otherwise, use the first variable from the file.
            # ------------------------------------------------------------------
            selected_var = request.POST.get("variable", variables[0] if variables else None)
            context["selected_var"] = selected_var

            # Get the data for the selected variable
            var_data = ds.variables[selected_var]

            # ------------------------------------------------------------------
            # Get the time axis if it exists
            # ------------------------------------------------------------------
            times = ds.variables["time"][:] if "time" in ds.variables else None
            context["times"] = times.tolist() if times is not None else None

            # ------------------------------------------------------------------
            # Determine which time step to display
            # If the user selected a time index in the form, use it
            # Default to 0 if not specified
            # ------------------------------------------------------------------
            selected_time_idx = int(request.POST.get("time_idx", 0))
            context["selected_time_idx"] = selected_time_idx

            # ------------------------------------------------------------------
            # Extract the 2D slice for the selected variable and time
            # This is where the user selection directly affects the plot:
            # Changing the variable or the time index will change data2d.
            # ------------------------------------------------------------------
            if times is not None:
                data2d = var_data[selected_time_idx, ...]  # slice at selected time
            else:
                data2d = var_data[:]  # no time axis, use all data

            # ------------------------------------------------------------------
            # Create a Plotly heatmap of the selected variable at the selected time
            # The user sees this plot in the template
            # ------------------------------------------------------------------
            fig = go.Figure()
            fig.add_trace(go.Heatmap(z=data2d))
            fig.update_layout(
                title=f"{selected_var} — Time step {selected_time_idx}",
                xaxis_title="Longitude",
                yaxis_title="Latitude",
                height=600
            )
            context["plot_html"] = fig.to_html(full_html=False)

            # ------------------------------------------------------------------
            # Gather metadata about the file for display
            # ------------------------------------------------------------------
            context["metadata"] = {
                "dimensions": list(ds.dimensions.keys()),
                "variables": list(ds.variables.keys()),
                "times": times.tolist() if times is not None else "None",
            }

            # Close the NetCDF file
            ds.close()

    # --------------------------------------------------------------------------
    # If GET request (first page load), show an empty form
    # --------------------------------------------------------------------------
    else:
        form = NetCDFUploadForm()

    # Add form to context so it can be rendered in the template
    context["form"] = form

    # --------------------------------------------------------------------------
    # Render the template with context
    # --------------------------------------------------------------------------
    return render(request, "uploader/upload.html", context)
