import os
import io
import json
from PIL import Image
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from .models import File, Folder

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


def get_folder_tree(folder):
    files={}
    for file in folder.files.all():
        files[str(file.file)]=str(file.description)
    return {
        "id":folder.id,
        "name":folder.name,
        "childfiles": files,
        "childfolders": [get_folder_tree(folder) for folder in folder.childfolder.all()]
    }

def get_file_tree():
    tree={}
    files = {}
    initial_folders = Folder.objects.filter(parent_folder__isnull=True)
    initial_files = File.objects.filter(folder__isnull=True)
    for folder in initial_folders:
        tree[folder.id] = get_folder_tree(folder)
    for file in initial_files:
        files[str(file.file)] = str(file.description)
    tree["files"]=files
    return tree

def save_to_json():
    """Сохранение всех объектов модели в JSON-файл."""
    data = get_file_tree()  # Получаем все объекты как список словарей
    print(data)
    with open("static/data/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    # Отправка обновлённых данных в WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "json_updates_group",
        {"type": "send_json_update", "data": data},
    )

@receiver(post_save, sender=File)
@receiver(post_save, sender=Folder)
@receiver(post_delete, sender=File)
@receiver(post_delete, sender=Folder)
def model_changed(sender, **kwargs):
    save_to_json()