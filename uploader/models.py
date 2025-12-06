from django.db import models

class NetCDFFile(models.Model):
    file = models.FileField(upload_to='netcdf/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.file)
