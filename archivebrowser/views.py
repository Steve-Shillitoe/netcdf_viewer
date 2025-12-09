from django.shortcuts import render
from django.http import HttpResponse

def radar_tree(request):
    tree = [
        {
            "name": "NXPOL1",
            "years": {
                "2025": {
                    "January": {
                        "01": ["img_001.png", "img_002.png"],
                        "02": ["img_101.png"]
                    },
                    "February": {
                        "10": ["storm_a.png", "storm_b.png"]
                    }
                }
            }
        },
        {
            "name": "NXPOL2",
            "years": {
                "2024": {
                    "December": {
                        "14": ["radar_01.png", "radar_02.png"],
                    }
                }
            }
        }
    ]

    return render(request, "archivebrowser/radar_tree.html", {"tree": tree})

# def print_pdf(request):
#     if request.method == "POST":
#         selected_files = request.POST.getlist("selected_files")
#         return HttpResponse(f"PDF Report requested for: {selected_files}")

#     return HttpResponse("No files selected.")


# def download_data(request):
#     if request.method == "POST":
#         selected_files = request.POST.getlist("selected_files")
#         return HttpResponse(f"Download requested for: {selected_files}")

#     return HttpResponse("No files selected.")