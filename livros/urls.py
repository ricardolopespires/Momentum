from django.urls import path
from . import views



app_name = 'livros'



urlpatterns = [

    path('livros/created/', views.create_livro, name = 'created'),
    path('livros/verificar/',views.verificar, name = 'verificar'),
    path('livros/<livro_id>/reviews/', views.add_review, name = 'add_review'),

    path('add/<pk>/wishlist/', views.add_playlist, name = 'add_playlist'),
    


    path('leitura/livros/recomendacoes/', views.recomendacoes, name = 'recomendacoes'),
    path('leitura/livros/favoritos/', views.favoritos, name = 'favoritos'),
    path('leitura/<livros_id>/favoritos/',views.add_favoritos, name = 'add_favoritos'),
    path('leitura/livros/playlist/', views.playlist, name = 'playlist'),
    path('leitura/livros/reviews/', views.reviews, name = 'reviews'),
    path('leitura/livros/discussoes/', views.discussoes, name = 'discussoes'),
    
    path('dashboard/leitura/',views.leitura, name = 'leitura'),
    path('leitura/<id_livro>/add/',views.add_leitura, name = 'add_leitura'),
    path('leitura/<int:pk>/details/', views.leitura_details, name = 'leitura_details'),
    path("<int:pk>/iniciar", views.iniciar_leitura,  name="iniciar_leitura" ),
    path("<int:pk>/pausar", views.pausar_leitura, name="pausar_leitura" ),
    path("<int:pk>/concluir", views.concluir_leitura, name="concluir_leitura"  ),
    path("<int:pk>/paginas/conluida/", views.paginas_conluida, name = 'paginas_conluida'),
        
    path('dashboard/<livro_id>/details', views.livro_dashboard_details, name = 'livro_dashboard_details'),

]