from rest_framework import serializers
from .models import File, Folder

# Сериалайзер для каталогов. Дополнительно создаем вычисляемые поля для дочерних каталогов и полного пути к каталогу
class FolderSerializer(serializers.ModelSerializer):
    childfolder = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()
    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent_folder', 'owner', 'created_at', 'files', 'childfolder', 'full_path']

    # Получаем все дочерние каталоги для текущего каталога и сериализируем их
    def get_childfolder(self, obj):
        # Рекурсивно сериализуем дочерние категории
        childfolder = obj.childfolder.all()
        return FolderSerializer(childfolder, many=True).data

    #  Получем словарь содержащий родительские имена каталогов и их идентификаторы
    def get_full_path(self, obj):
        path = {}
        current = obj
        while current:
            path[current.id] = current.name
            current = current.parent_folder
        return path

# Сериалайзер для файлов
class FileSerializer(serializers.ModelSerializer):
    folder = FolderSerializer()
    class Meta:
        model = File
        fields = ['id', 'description', 'file', 'uploaded_at', 'folder']
