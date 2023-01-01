"""Momentum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.indextemplateview, name = 'index'),


    #------------------ Livros -----------------------------------------------------
    path('livros/lancamentos/',views.livros, name = 'livros'),
    path('livros/mais-livros/',views.mais_lido, name = 'mais_lido'),
    path('livros/autores/', views.autores, name = 'autores'),
    path('livros/ranking/', views.ranking, name = 'ranking'),
    path('livros/<livro_id>/details', views.livro_details, name = 'livro_details'),
    path('',include('analytics.urls', namespace = 'analytics')),       
    

    #----------------------- Movie -----------------------------------------------------
    path('livros/filmes/', views.movie, name = 'movie'),
    path('livros/filmes/cinema', views.cinema, name = 'cinema'),
    path('livros/filmes/breve/',views.breve, name = 'breve'),
    path('livros/filmes/trailler/', views.trailler, name = 'trailler'),
    #path('livros/filmes/<id_trailler>/trailler/', views.video,  name = 'video'),
    #path('livros/filmes/<int:pk>/details', views.movie_details, name = 'movie_details'),   



    #------------------------- Accounts --------------------------------------------------

    path('',include('accounts.urls')),

    
    #---------------------------------- Newsletter ----------------------------------------
    path('newsletter/', views.newsletter, name = 'newsletter'),




    #------------  Dashboard  --------------------------------------------------------------
    path('', include('dashboard.urls', namespace = 'dashboard')),
    path('livros/',include('livros.urls', namespace = 'livros')),   
    path('director', include('director.urls', namespace = 'director')),
    path('actor', include('actor.urls', namespace = 'actor')),
    path('movie', include('movie.urls', namespace = 'movie')),

    

    #-----------------------------------------MANAGEMENT --------------------
    path('',include('management.urls', namespace = 'management')),
    #path('movie/',include('movie.urls', namespace = 'movie')),
    #path('analytics/', include('analytics.urls', namespace = 'analytics')),


    
]
if settings.DEBUG:
    urlpatterns  += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
