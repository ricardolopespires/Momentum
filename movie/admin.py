from django.contrib import admin
from movie.models import Movie, Trailler, Review, Like
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    list_display = ['Title','Average_Rating','Average_Count']
    list_filter = ['Title']
    search_fields = ['Title']


@admin.register(Trailler)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = ['user','movie','date']
    list_filter = ['user','movie','date']
    search_fields = ['user','movie','date']


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = ['user','movie','date']
    list_filter = ['user','movie','date']
    search_fields = ['user','movie','date']



admin.site.register(Like)

