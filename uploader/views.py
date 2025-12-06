import os
from django.shortcuts import render
from django.conf import settings
from .forms import NetCDFUploadForm
from netCDF4 import Dataset
import plotly.graph_objects as go

def upload_netcdf(request):
    context = {
        "variables": None,
        "selected_var": None,
        "times": None,
        "selected_time_idx": None,
        "metadata": None,
        "plot_html": None,
        "nc_filename": None,
    }

    if request.method == "POST":
        form = NetCDFUploadForm(request.POST, request.FILES)

        # Check if a new file was uploaded
        if 'file' in request.FILES and form.is_valid():
            nc_file = request.FILES["file"]
            save_path = os.path.join(settings.MEDIA_ROOT, nc_file.name)
            with open(save_path, "wb+") as f:
                for chunk in nc_file.chunks():
                    f.write(chunk)
            nc_path = save_path

        # Otherwise use existing file (from hidden input)
        elif 'existing_file' in request.POST:
            nc_path = request.POST['existing_file']
        else:
            nc_path = None

        if nc_path and os.path.exists(nc_path):
            context["nc_filename"] = nc_path
            ds = Dataset(nc_path, "r")

            # Get plottable variables
            variables = [v for v in ds.variables.keys() if len(ds.variables[v].dimensions) >= 2]
            context["variables"] = variables

            # Selected variable
            selected_var = request.POST.get("variable", variables[0] if variables else None)
            context["selected_var"] = selected_var

            var_data = ds.variables[selected_var]

            # Time axis
            times = ds.variables["time"][:] if "time" in ds.variables else None
            context["times"] = times.tolist() if times is not None else None

            # Selected time index
            selected_time_idx = int(request.POST.get("time_idx", 0))
            context["selected_time_idx"] = selected_time_idx

            # Extract slice
            if times is not None:
                data2d = var_data[selected_time_idx, ...]
            else:
                data2d = var_data[:]

            # Build Plotly heatmap
            fig = go.Figure()
            fig.add_trace(go.Heatmap(z=data2d))
            fig.update_layout(title=f"{selected_var} — Time step {selected_time_idx}", height=600)
            context["plot_html"] = fig.to_html(full_html=False)

            # Metadata
            context["metadata"] = {
                "dimensions": list(ds.dimensions.keys()),
                "variables": list(ds.variables.keys()),
                "times": times.tolist() if times is not None else "None",
            }

            ds.close()

    else:
        form = NetCDFUploadForm()

    context["form"] = form
    return render(request, "uploader/upload.html", context)
