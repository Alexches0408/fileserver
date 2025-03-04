from rest_framework import serializers
from .models import File, Folder

# Сериалайзер для каталогов. Дополнительно создаем вычисляемые поля для дочерних каталогов и полного пути к каталогу
class FolderSerializer(serializers.ModelSerializer):
    childfolder = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()
    file_tree = serializers.SerializerMethodField()
    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent_folder', 'owner', 'created_at', 'files', 'childfolder', 'full_path', 'file_tree', 'deleted']

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

    def get_folder_tree(self, folder):
        files={}
        for file in folder.files.all():
            files[str(file.description)]=str(file.file)
        return {
            "id":folder.id,
            "name":folder.name,
            "childfiles": files,
            "childfolders": [self.get_folder_tree(folder) for folder in folder.childfolder.all()]
        }

    def get_file_tree(self, obj):
        tree={}
        files = {}
        initial_folders = Folder.objects.filter(parent_folder__isnull=True)
        initial_files = File.objects.filter(folder__isnull=True)
        for folder in initial_folders:
            tree[folder.id] = self.get_folder_tree(folder)
        for file in initial_files:
            files[str(file.description)] = str(file.file)
        tree["files"]=files
        return tree



# Сериалайзер для файлов
class FileSerializer(serializers.ModelSerializer):
    folder = FolderSerializer()
    class Meta:
        model = File
        fields = ['id', 'description', 'file', 'uploaded_at', 'folder', 'deletedfile', 'thumbnail', 'icon']
