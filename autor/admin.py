from django.contrib import admin
from .models import Autor
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Autor)
class ActorAdmin(ImportExportModelAdmin):
    list_display = ['id', 'nome']
    list_filter = ['id', 'nome']
    search_fields = ['id', 'nome']
    prepopulated_fields = {'slug':('nome',)}
