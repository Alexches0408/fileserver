from django.db import models
from django.conf import settings



# Create your models here.

class Folder(models.Model):
    name = models.CharField(max_length=100)
    parent_folder = models.ForeignKey('self', related_name="childfolder", null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    folder = models.ForeignKey(Folder, related_name='files', null=True, blank=True, on_delete=models.CASCADE)
    is_processing_thumbnail = models.BooleanField(default=False)
    deletedfile = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description if self.description else f"File {self.id}"



