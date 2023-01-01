from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Ebook, Playlist, Capitulo, Review, Leitura, Favoritos, Livros_Analytics
from .models import Question, Answer, Quiz

# Register your models here.





@admin.register(Ebook)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['id','titulo','status','classificacao','views']
    search_fields = ['titulo']


@admin.register(Review)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['livro','rate']
    search_fields =['livro']


@admin.register(Playlist)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['user']




@admin.register(Leitura)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['livro','duracao']
    search_fields = ['livro']


@admin.register(Favoritos)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['livro','user']


@admin.register(Capitulo)
class ChapterAdmin(ImportExportModelAdmin):
    list_display = ['id','order','titulo','duracao','leitura' ]
    search_fields = ['title']




@admin.register(Livros_Analytics)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ['id','title', 'average_rating','average_count']
    search_fields = ['title']




class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin):
    list_display = ['name', 'status','topic', 'number_of_questions']
    search_fields = ['name']


'''
@admin.register(Question)
class QuizAdmin(ImportExportModelAdmin):
    list_display = ['text', ]
    search_fields = ['text']

'''
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)