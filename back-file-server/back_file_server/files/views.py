from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import File, Folder
from .serializers import FolderSerializer, FileSerializer
from .filters import FileModelFilter, FolderModelFilter

# Создаем вьюсет для файлов. Здесь же определяем фильтры и разрешения
class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileModelFilter
    permission_classes = [IsAuthenticated]

    # переопределяем метод загрузки файла чтобы можно было загружать по несколько файлов
    # Поочередно для каждого файла создаем экземпляры объектов
    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        folder_id = request.data.get('folder')
        file_instances = []
        for uploaded_file in files:
            if folder_id != "null":
                file_instance = File.objects.create(
                    description=uploaded_file.name,
                    file=uploaded_file,
                    folder=Folder.objects.get(id=folder_id)
                )
            else:
                file_instance = File.objects.create(
                    description=uploaded_file.name,
                    file=uploaded_file,
                )
            file_instances.append(file_instance)

        serializer = self.get_serializer(file_instances, many=True)
        return Response(serializer.data, status=201)



# Вьюсет для каталогов. Определяем фильтры и разрешения
class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FolderModelFilter
    permission_classes = [IsAuthenticated]

# Переопределяем метод создания каталога чтобы отличать каталоги имеющие родителей от
# не имеющих
    def create(self, request, *args, **kwargs):
        folder_name = request.data.get('name')
        parent_folder = request.data.get('parent_folder')
        if parent_folder and parent_folder!="null":
            folder_instance = Folder.objects.create(
                name=folder_name,
                parent_folder=Folder.objects.get(id=parent_folder),
            )
        else:
            folder_instance = Folder.objects.create(
                name=folder_name
            )

        serializer = self.get_serializer(folder_instance)
        return Response(serializer.data, status=201)

    # Определяем метод для получения всех дочерних файлов и каталогов текущего каталога
    # Данные получаем по url: /files/folder/<id>/content_folder
    @action(detail=True, methods=['get'])
    def content_folder(self, request, pk):
        folder = self.get_object()
        childfolders=folder.childfolder.all()
        files=folder.files.all()
        return Response({
            "childfolders": FolderSerializer(childfolders, many=True).data,
            "files": FileSerializer(files, many=True).data,
        })


