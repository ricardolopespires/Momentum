from django.urls import path
from . import views


app_name = 'dashboard'



urlpatterns  = [

        path('dashboard/', views.dashboard, name = 'manager'),
        path('list/livros/',views.Lista_Livros_View.as_view(), name = 'list_livros'),
        path('livro/<livro_id>/detail/', views.Livro_Detial_View.as_view(), name = 'livro_detail'),           
        
        

]