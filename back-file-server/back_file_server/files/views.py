from contextlib import nullcontext

from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .forms import FileUploadForm, FolderForm
from .models import File, Folder
from .serializers import FolderSerializer, FileSerializer
from .filters import FileModelFilter, FolderModelFilter

# Сериалайзер для файлов
class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileModelFilter
    permission_classes = [IsAuthenticated]

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
                print(file_instance.file)
            else:
                file_instance = File.objects.create(
                    description=uploaded_file.name,
                    file=uploaded_file,
                )
                print(file_instance.file)
            file_instances.append(file_instance)

        serializer = self.get_serializer(file_instances, many=True)
        return Response(serializer.data, status=201)



# Сериалайзер для папок
class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FolderModelFilter
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        folder_name = request.data.get('name')
        parent_folder = request.data.get('parent_folder')
        print(f'Значение родительского каталога: {parent_folder}')
        if parent_folder and parent_folder!="null":
            print("Создаем объект с родительским полем")
            folder_instance = Folder.objects.create(
                name=folder_name,
                parent_folder=Folder.objects.get(id=parent_folder),
            )
        else:
            print("Создаем объект с незаполненным родительским полем")
            folder_instance = Folder.objects.create(
                name=folder_name
            )

        serializer = self.get_serializer(folder_instance)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['get'])
    def content_folder(self, request, pk):
        folder = self.get_object()
        childfolders=folder.childfolder.all()
        files=folder.files.all()
        return Response({
            "childfolders": FolderSerializer(childfolders, many=True).data,
            "files": FileSerializer(files, many=True).data,
        })





# Для удаления файла
def delete_file(request, file_id):
    if request.method == "POST":
        file = get_object_or_404(File, id=file_id)
        file.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

# Для удаления папки
def delete_folder(request, folder_id):
    if request.method == "POST":
        folder = get_object_or_404(Folder, id=folder_id)
        folder.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

# Для загрузки файла
def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data["file_field"]
            for f in files:
                file = File.objects.create(file=f, description=f.name)
                # if currentpath:
                #     folder = Folder.objects.get(pk=currentpath)
                #     file.folder=folder
                file.save()
            return JsonResponse({"success": True, "message": "Форма успешно обработана!"})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "message": "Только POST-запросы поддерживаются."})

# Для создания папки
@csrf_exempt
def create_folder(request):
    if request.method == "POST":
        form = FolderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.owner=request.user
            form.save()
            return JsonResponse({"success": True, "message": "Форма успешно обработана!"})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "message": "Только POST-запросы поддерживаются."})


# Основной обработчик. Обрабатывает основной шаблон сайта, загрузку файлов и создание каталогов
def file_list(request, pk=0):
# Определяем текущий каталог и какие файлы и папки в нём содержатся
    currentpath = int(str(request.path).replace('/files/folder', '').replace('/', ''))
    if currentpath:
        folders = Folder.objects.filter(parent_folder__id = currentpath)
        files = File.objects.filter(folder__id=currentpath)
    else:
        folders = Folder.objects.filter(parent_folder__isnull=True)
        files = File.objects.filter(folder__isnull=True)
    create_folder_form = FolderForm()
    upload_file_form = FileUploadForm()
# Определяем адрес родительского каталога
    if currentpath:
        parrentfolder = Folder.objects.get(id=currentpath).parent_folder
        if parrentfolder:
            parrentfolder = "/files/folder/" + str(parrentfolder.id)
        else:
            parrentfolder ="/files/folder/0"
    else:
        parrentfolder = None
# Обработка POST-запроса. Проверяем условия, и либо создаём папку либо загружаем файлы
#     if request.method == 'POST':
#         if 'create_folder' in request.POST:
#             create_folder_form = FolderForm(request.POST)
#             if create_folder_form.is_valid():
#                 if next((folder for folder in folders if create_folder_form.cleaned_data['name']==folder.name), None):
#                     messages.success(request, "Каталог с таким названием уже существует!")
#                 else:
#                     folder = create_folder_form.save(commit=False)
#                     folder.owner = request.user
#                     if currentpath:
#                         folder.parent_folder = Folder.objects.get(id = currentpath)
#                     folder.save()
#             else:
#                 create_folder_form = FolderForm()
#
#         elif 'upload_file' in request.POST:
#             upload_file_form = FileUploadForm(request.POST, request.FILES)
#             if upload_file_form.is_valid():
#                 files = upload_file_form.cleaned_data["file_field"]
#                 for f in files:
#                     file = File.objects.create(file=f, description=f.name)
#                     if currentpath:
#                         folder = Folder.objects.get(pk=currentpath)
#                         file.folder=folder
#                     file.save()
#
#         return redirect(request.path)


    return render(request, 'file_list.html',
                  {'files': files, 'folders': folders, 'create_folder_form': create_folder_form,
                   'upload_file_form': upload_file_form, 'parrentfolder':parrentfolder})

