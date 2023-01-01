from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Editora
# Register your models here.


@admin.register(Editora)
class EditoraAdmin(ImportExportModelAdmin):
    list_display = ['id', 'nome']
    list_filter = ['id', 'nome']
    search_fields = ['id', 'nome']
    prepopulated_fields = {'slug':('nome',)}
