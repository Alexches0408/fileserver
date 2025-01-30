from django.db import models
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os



# Create your models here.

class Folder(models.Model):
    name = models.CharField(max_length=100)
    parent_folder = models.ForeignKey('self', related_name="childfolder", null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    folder = models.ForeignKey(Folder, related_name='files', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.description if self.description else f"File {self.id}"


# Сигнал для удаления файла после удаления объекта
@receiver(post_delete, sender=File)
def delete_file_from_system(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        try:
            os.remove(instance.file.path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")