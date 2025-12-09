"""
A request is initially received by a web server, which then forwards it to the Django application 
via the WSGI interface. 

The Django application then matches the requested URL to a specific view function in the file views.py 
using the URL-view function mappings in the file urls.py.

Once the URL is matched, Django calls the associated view function.
The view function processes the request and generates a HTTP response.

If the view needs to render a template, it utilizes Django's template engine.
The template engine combines the view's data with the specified template, 
generating the final HTML content to be sent in the response.
Templates are HTML files in which executable commands are enclosed in {% %} 
and context variables are enclosed in {{}}. 
When a template is rendered into a web page, the context variables are replaced by a value or a string.

This response is then sent back through the web server to the client's browser.


netcdf_viewer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#include('uploader.urls') tells Django to use the URL patterns defined in the uploader app
#static() allows uploaded files and generated plots to be served while in development

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('uploader.urls')),
    path("archive/", include("archivebrowser.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
