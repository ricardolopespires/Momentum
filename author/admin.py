from django.contrib import admin
from .models import Author
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Author)
class ActorAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['id', 'name']
    search_fields = ['id', 'name']
    prepopulated_fields = {'slug':('name',)}
