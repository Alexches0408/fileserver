from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'files',views.FileViewSet,basename='file')
router.register(r'folders',views.FolderViewSet,basename='folder')


urlpatterns = [
    path('folder/0/', views.file_list, name='file_list'),
    path('folder/<int:pk>/', views.file_list, name='folder_detail'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('',include(router.urls))
]