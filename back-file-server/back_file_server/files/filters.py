from django_filters import rest_framework as filters
from .models import File, Folder

# Фильтр для файлов. Если мы на главной, получаем все файлы без поля folder
# Если находимся в каталоге, получаем все файлы с полем folder равным текущему каталогу
class FileModelFilter(filters.FilterSet):
    folder_is_empty = filters.BooleanFilter(
        field_name="folder",
        method="filter_folder_is_empty",
        label="Folder is empty"
    )
    folder_id = filters.NumberFilter(field_name="folder__id", label="Folder ID")


    class Meta:
        model = File
        fields = ['folder_is_empty', 'folder_id']

    def filter_folder_is_empty(self, queryset, folder, value):
        # Если value = True, возвращаем записи, где поле name пустое или None
        if value:
            return queryset.filter(folder__isnull=True)
        # Если value = False, возвращаем записи, где поле name заполнено
        return queryset.filter(folder__isnull=False)


# Фильтр для каталогов. Если мы на главной, получаем все каталоги без родителя
# Если находимся в каталоге, получаем все файлы с родителем, равным текущему каталогу
class FolderModelFilter(filters.FilterSet):
    parent_folder_is_empty = filters.BooleanFilter(
        field_name="parent_folder",
        method="filter_folder_is_empty",
        label="Parent folder is empty"
    )


    parent_folder_id = filters.NumberFilter(field_name="parent_folder__id", label="ParentFolder ID")

    class Meta:
        model = Folder
        fields = ['parent_folder_is_empty', 'parent_folder_id']

    def filter_folder_is_empty(self, queryset, folder, value):
        # Если value = True, возвращаем записи, где поле name пустое или None
        if value:
            return queryset.filter(parent_folder__isnull=True)
        # Если value = False, возвращаем записи, где поле name заполнено
        return queryset.filter(parent_folder__isnull=False)

