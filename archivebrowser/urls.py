# archivebrowser/urls.py
from django.urls import path
from .views import radar_tree

urlpatterns = [
    path("", radar_tree, name="radar_tree"),
]
