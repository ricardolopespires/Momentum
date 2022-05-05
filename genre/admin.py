from django.contrib import admin
from .models import Genre
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(Genre)
class AdminGenre(ImportExportModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug':['title',]}