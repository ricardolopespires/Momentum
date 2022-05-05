from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Ebook, Playlist, Review, Leitura, Favoritos

# Register your models here.





@admin.register(Ebook)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['Title']


@admin.register(Review)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['livro','user']


@admin.register(Playlist)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['user']




@admin.register(Leitura)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['livro','user']


@admin.register(Favoritos)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['livro','user']

