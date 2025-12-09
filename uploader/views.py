from django.shortcuts import render
from .forms import NetCDFUploadForm
from .models import NetCDFFile
from netCDF4 import Dataset
import plotly.graph_objects as go

def upload_netcdf(request):

    context = {}

    if request.method == "POST":

        form = NetCDFUploadForm(request.POST, request.FILES)
        context["form"] = form

        # --------------------------------------------------------------
        # CASE 1: NEW UPLOAD
        # --------------------------------------------------------------
        if "file" in request.FILES:

            nc_instance = NetCDFFile.objects.create(file=request.FILES["file"])
            context["nc_file_instance"] = nc_instance
            ds = Dataset(nc_instance.file.path, "r")

        # --------------------------------------------------------------
        # CASE 2: VARIABLE/TIME CHANGE
        # --------------------------------------------------------------
        else:
            file_id = request.POST.get("existing_file_id")

            if not file_id:
                # Should never happen if template includes hidden field
                return render(request, "uploader/upload.html", context)

            nc_instance = NetCDFFile.objects.get(id=file_id)
            context["nc_file_instance"] = nc_instance
            ds = Dataset(nc_instance.file.path, "r")

        # --------------------------------------------------------------
        # Shared processing
        # --------------------------------------------------------------

        # Variables that can be plotted
        variables = [
            v for v in ds.variables.keys()
            if len(ds.variables[v].dimensions) >= 2
        ]
        context["variables"] = variables

        selected_var = request.POST.get("variable", variables[0])
        context["selected_var"] = selected_var

        var_data = ds.variables[selected_var]

        # Time axis
        times = ds.variables["time"][:] if "time" in ds.variables else None
        context["times"] = times.tolist() if times is not None else None

        selected_time_idx = int(request.POST.get("time_idx", 0))
        context["selected_time_idx"] = selected_time_idx

        # selected time value passed separately
        context["selected_time"] = (
            times[selected_time_idx] if times is not None else None
        )

        # 2D slice
        if times is not None:
            data2d = var_data[selected_time_idx, ...]
        else:
            data2d = var_data[:]

        # Plotly heatmap
        fig = go.Figure()
        fig.add_trace(go.Heatmap(z=data2d))
        fig.update_layout(
            title=f"{selected_var} — Time step {selected_time_idx}",
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            height=600,
        )
        context["plot_html"] = fig.to_html(full_html=False)

        # Metadata
        context["metadata"] = {
            "dimensions": list(ds.dimensions.keys()),
            "variables": list(ds.variables.keys()),
            "times": times.tolist() if times is not None else "None",
        }

        ds.close()
        return render(request, "uploader/upload.html", context)

    # GET request
    context["form"] = NetCDFUploadForm()
    return render(request, "uploader/upload.html", context)
