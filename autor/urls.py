from django.urls import path
from . import views




app_name = 'author'



urlpatterns = [

    path('author/verificar/', views.verificar, name = 'verificar'),
    path('author/adicionar/', views.created, name = 'adicionar'),

]
