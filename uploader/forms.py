# uploader/forms.py
from django import forms
from .models import NetCDFFile

class NetCDFUploadForm(forms.ModelForm):
    class Meta:
        model = NetCDFFile
        fields = ['file']

