from django.shortcuts import render, reverse, get_object_or_404 
#from django.views.generic import View, TemplateView, ListView ,DeleteView
#from movie.models import Movie, Trailler
from livros.models import Ebook, Review
from autor.models import Autor
from django.core.paginator import Paginator
#from accounts.forms import NewsletterForm
#from accounts.models import User, Newsletter
from django.db.models import F, Sum, Q
from django.template import loader
from django.db.models import Avg
from django.http import HttpResponseRedirect
import datetime
from datetime import date

#from dashboard.recomentador import content_recommender, recommender_20


def indextemplateview(request):
    livros = Ebook.objects.all()
    return render(request, 'initial/index.html', {'livros':livros })


def livros(request):
    return render(request, 'initial/livros/lancamentos.html')


def mais_lido(request):
    livros = Ebook.objects.all().order_by('-Popularity')
    return render(request, 'initial/livros/mais_lido.html', {'livros':livros})


def autores(request):
    autores = Autor.objects.all()
    return render(request, 'initial/livros/autores.html',{'autores':autores})


def ranking(request):
    livros = Ebook.objects.all().order_by('-Votes_Count')
    return render(request, 'initial/livros/ranking.html', {'livros': livros})



def livro_details(request, livro_id):
    livro = get_object_or_404(Ebook, id = livro_id)
    reviews = Review.objects.filter(livro = livro)
    reviews_avg = reviews.aggregate(Avg('rate'))['rate__avg']

    if reviews_avg == None:
        reviews_avg = 0
    else:
        reviews_avg

    
    livro.Average_Rating = str(reviews_avg)
    livro.Average_Count = str(reviews_avg /10)
    livro.Votes_Count = reviews.count()    
    livro.save()

    title = str(livro.titulo)
   
    #recomendacoes = content_recommender(title)


    return render (request, 'initial/livros/details.html',{

        'livro':livro, 'reviews':reviews, 'reviews_avg':reviews_avg,
        #'recomendacoes':recomendacoes, 

        })


#-----------------------------------------  Movie -----------------------------

def movie(request):
    #movies = Movie.objects.all()    
    return render( request, 'initial/movie/filmes.html')


def cinema(request):
    #data_atual = date.today()
    #ano = "{}".format(data_atual.year)   
    #movies = Movie.objects.filter(Publish__year=ano) 
    return render(request, 'initial/movie/cinema.html')



def breve(request):
    return render(request, 'initial/movie/breve.html')



def trailler(request):
    #trailler = Trailler.objects.all()   
    return render (request, 'initial/movie/trailler.html')


def video(request, id_trailler):
    movie = get_object_or_404(Trailler, id = id_trailler)
    return render(request, 'initial/movie/video.html',{'movie': movie})



def movie_details(request, pk):
    movie = get_object_or_404(Movie, id = pk)
    return render (request, 'initial/movie/details.html',{'movie': movie })

#------------------------------------- Newsletter -----------------------------


def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST or None)
        if form.is_valid():
            newsletter = form.save(commit=False)                        
            email = form.cleaned_data['email']            
            print(email)
            if Newsletter.objects.filter(email = email).exists():
                return HttpResponseRedirect(reverse('index'))

            elif User.objects.filter(email = email).exists():
                newsletter.email = email
                newsletter.user = request.user
                newsletter.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                newsletter.email = email                
                newsletter.save()
    else:
        form = NewsletterForm()
    return render(request, 'initial/index.html', {'form':form})    
                

