from rest_framework import serializers
from .models import File, Folder


class FolderSerializer(serializers.ModelSerializer):
    childfolder = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()
    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent_folder', 'owner', 'created_at', 'files', 'childfolder', 'full_path']

    def get_childfolder(self, obj):
        # Рекурсивно сериализуем дочерние категории
        childfolder = obj.childfolder.all()
        return FolderSerializer(childfolder, many=True).data

    def get_full_path(self, obj):
        path = {}
        current = obj
        while current:
            path[current.id] = current.name
            current = current.parent_folder
        return path

class FileSerializer(serializers.ModelSerializer):
    folder = FolderSerializer()
    class Meta:
        model = File
        fields = ['id', 'description', 'file', 'uploaded_at', 'folder']
