from django.urls import path
from . import views
from . import api



app_name = 'livros'



urlpatterns = [

    path('created/', views.create_livro, name = 'created'),
    path('verificar/',views.verificar, name = 'verificar'),
    path('livros/opcao/adicionar/',views.Opcao_Create_View.as_view(), name = 'opcao'),
    path('livros/<livro_id>/reviews/', views.add_review, name = 'add_review'),
    path('livros/created/amazon/', views.Create_Amazon_View.as_view(), name = 'amazon'),
    path('livros/created/z-library/', views.Create_zlibrary_View.as_view(), name = 'z-library'),
    path('add/<pk>/wishlist/', views.add_playlist, name = 'add_playlist'),
    


    path('leitura/livros/recomendacoes/', views.recomendacoes, name = 'recomendacoes'),
    path('leitura/livros/favoritos/', views.favoritos, name = 'favoritos'),
    path('leitura/<livros_id>/favoritos/',views.add_favoritos, name = 'add_favoritos'),
    path('leitura/livros/playlist/', views.playlist, name = 'playlist'),
    path('leitura/livros/reviews/', views.reviews, name = 'reviews'),
    path('leitura/livros/discussoes/', views.discussoes, name = 'discussoes'),
    
    path('dashboard/leitura/',views.Leitura_List_View.as_view(), name = 'leitura'),
    path('leitura/<id_livro>/add/',views.add_leitura, name = 'add_leitura'),
    path('leitura/<leitura_id>/details/', views.Leitura_Detail_View.as_view(), name = 'leitura_details'),
    path("<int:pk>/iniciar", views.iniciar_leitura,  name="iniciar_leitura" ),
    path("<int:pk>/pausar", views.pausar_leitura, name="pausar_leitura" ),
    path("<int:pk>/concluir", views.concluir_leitura, name="concluir_leitura"  ),
    path("<pagina_id>/paginas/conluida/", views.paginas_conluida, name = 'paginas_conluida'),

    path('<leitura_id>/<questao_id>/livros/perguntas/respostas/',views.Quiz_Data_View.as_view(), name ='questoes'),
    
    
        
    path('dashboard/<livro_id>/details', views.livro_dashboard_details, name = 'livro_dashboard_details'),


    path('livro/leitura/<leitura_id>/paginas/', views.Leitura_Pagina_View.as_view(), name = 'leitura-paginas'),
    path('livro/leitura/<leitura_id>/create/',views.Create_Pagina_View.as_view(), name = 'create_paginas'),
    path('livro/leitura/<pagina_id>/pagina/',views.Pagina_leitura_View.as_view(), name = 'texto-pagina'),

    #------------------------------------------------- API Livro --------------------------------------------

     path('api/', api.LivroListAPIView.as_view(), name="list"), 


]