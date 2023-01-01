from import_export.admin import ImportExportModelAdmin
from .models import Categoria, Genero
from django.contrib import admin



# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['id', 'titulo','quantidade']
    list_filter = ['titulo']
    search_fields = ['id', 'titulo']
    prepopulated_fields = {'slug':('id',)}


@admin.register(Genero)
class GeneroAdmin(ImportExportModelAdmin):
    list_display = [ 'titulo', 'categoria']
    list_filter = ['categoria']
    search_fields = ['id', 'titulo']
    prepopulated_fields = {'slug':('titulo',)}

