from django.urls import path
from . import views



app_name = 'management'



urlpatterns = [


	path('management/',views.Management_View.as_view(), name = 'index'),
	path('management/list/livros/',views.Lista_Livros_View.as_view(), name = 'list_livros'),
    path('management/livro/<livro_id>/detail/', views.Livro_Detial_View.as_view(), name = 'livro_detail'),

    path('management/livro/<livro_id>/created/',views.Created_Quiz_View.as_view(), name = 'created'),    


]

