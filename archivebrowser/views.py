from django.shortcuts import render

def radar_tree(request):
    """
    Build a hierarchical tree of radar images and pass it to the template.
    Leaf nodes include the image URL so we can display it on click.
    """
    # Define the tree with image URLs
    tree = {
        "NXPOL1": {
            "2025": {
                "December": {
                    "06": [
                        {"name": "radarImage1.png", "url": "/media/radarImage1.png"},
                        {"name": "radarImage2.png", "url": "/media/radarImage2.png"}
                    ],
                    "07": [
                        {"name": "radarImage3.png", "url": "/media/radarImage3.png"}
                    ],
                }
            }
        },
        "NXPOL2": {
            "2025": {
                "December": {
                    "06": [
                        {"name": "radarImage4.png", "url": "/media/radarImage4.png"}
                    ]
                }
            }
        }
    }

    # Pass the tree to the template
    context = {
        "tree": tree
    }
    return render(request, "archivebrowser/radar_tree.html", context)
