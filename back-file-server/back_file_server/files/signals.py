import os
import io
from PIL import Image
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from .models import File

# Удаление файлов и миниатюр из медиа после удаления объектов из базы
@receiver(post_delete, sender=File)
def delete_file_from_system(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        try:
            os.remove(instance.file.path)
            if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
                os.remove(instance.thumbnail.path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")

# Создаём миниаютюры для загружаемых изображений
@receiver(post_save, sender=File)
def create_thumbnail(sender, instance, created, **kwargs):
    if created and not instance.is_processing_thumbnail:
        instance.is_processing_thumbnail = True
        instance.save(update_fields=['is_processing_thumbnail'])
        if instance.file and instance.file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            with open(instance.file.path, "rb") as f:
                img_bytes = io.BytesIO(f.read())
            with Image.open(img_bytes) as img:
                img.thumbnail((100, 100))
                thumbname = f"thumb_{os.path.basename(instance.file.name)}"
                thumbpath = os.path.join('', thumbname)
                thumb_io = ContentFile(b'')
                img.save(thumb_io, format='JPEG')
                thumb_io.seek(0)
                instance.thumbnail.save(thumbpath,thumb_io)
        instance.is_processing_thumbnail = False
        instance.save(update_fields=['is_processing_thumbnail'])

# Определяем иконку файла в зависимости от расширения
def get_file_icon(file_name):
    extension = file_name.split('.')[-1].lower()
    icons = {
        'pdf': 'pdf-icon.png',
        'docx': 'word-icon.png',
        'doc':'word-icon.png',
        'xls':'excel-icon.png',
        'xlsx': 'excel-icon.png',
        'mp4': 'video-icon.png',
    }
    return icons.get(extension, 'default-icon.png')

# Присваиваем файлы иконок в базе
@receiver(post_save, sender=File)
def assign_file_icon(sender, instance, created, **kwargs):
    if created:
        file_icon = get_file_icon(instance.file.name)
        instance.icon = file_icon
        instance.save()
