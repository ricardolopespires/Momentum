from django.shortcuts import render, get_object_or_404, redirect
from .models import Ebook, Playlist, Review, Favoritos, Leitura
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import F, Sum, Q
from datetime import datetime, date
from django.contrib import messages
from author.models import Author
from django.db.models import Avg
from accounts.models import User
from django.urls import reverse
from genre.models import Genre
from .forms import ReviewForm
from datetime import datetime
from .forms import EbookForm
import datetime as dt
import random


# Create your views here.

@login_required
def livro_dashboard_details(request, livro_id):
    livro = get_object_or_404(Ebook, id = livro_id)
    leituras = Leitura.objects.filter(livro = livro)
    for leitura in leituras:
        livro.total_horas = leitura.duracao_total
        livro.save()  

    return render(request, 'livros/livro_dashboard_details.html',{'livro':livro})



@login_required
def verificar(request):
    if request.method=='POST':
        titulo = request.POST.get("titulo")
        print(titulo)

        if Ebook.objects.filter(Title = titulo).exists():
            messages.error(request,'Ops...., esse livro já foi adicionado, mais você pode ver a suas informações')
            return render(request, 'livros/verificar.html')

        else:
            messages.success(request, 'Legal o seu livro ainda não foi adicionado, vamos adicionar')
            return HttpResponseRedirect(reverse('livros:created'))
    
    return render(request, 'livros/verificar.html')

    
@login_required    
def create_livro(request):
    genre = Genre.objects.all()
    author = Author.objects.all()    
    number = "LIV" + str(random.randint(0,1000))


    if request.method == "POST":        
        titulo = request.POST.get("Title")      
        descricao = request.POST.get("Descricao")
        publish = request.POST.get("Publish")
        publish = datetime.strptime(publish, '%d/%m/%Y').date()
        poster = request.POST.get("Poster")
        poster_url = request.POST.get("Poster_url")
        genre = request.POST.getlist("genero")
        print(genre)
        service = request.POST.getlist("services")
        print("service",service)
        ids_genre = list(map(int, genre))
        edicao = request.POST.get('Edicao')
        autor = request.POST.getlist("autor")
        print(autor)
        ids_autor = list(map(int, autor))
        editora = request.POST.get("Editora")
        linguagem = request.POST.get("Linguagem")
        paginas = request.POST.get("Paginas")
        isbn = request.POST.get("ISBN")

        livro = Ebook(
            id = number,
            Title = titulo,
            Descricao = descricao,
            Publish = publish,
            Poster = poster,
            Poster_url = poster_url,
            Edicao = edicao,
            Editora = editora,
            Linguagem = linguagem,
            Paginas = paginas,
            ISBN = isbn, 
        )
        livro.save()

        if len(ids_genre):
            for genre in ids_genre:
                livro.Genero.add(genre)      

        if len(ids_autor):
            for autor in ids_autor:               
                livro.Autor.add(autor)      

        livro.user.add(request.user)

        request.user.livros.add(livro)
        request.user.Publicacoes += 1
        request.user.save()
        return HttpResponseRedirect(reverse('dashboard:manager'))


    else:
        return render(request, 'livros/created.html', { 'genre':genre, 'author':author, })



@login_required
def add_review(request, livro_id):
    if request.user.is_authenticated:
        username = get_object_or_404(User, name = request.user)
        print( username )
        livros = get_object_or_404(Ebook, id = livro_id)
        livro = Ebook.objects.get(id = livro_id)        
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)              
                data.rate = request.POST["rate"]
                data.user =  username
                data.livro = livro
                data.save()
                return redirect("livro_details", livro_id)
        else:
            form = ReviewForm()
        return render(request, 'initial/livros/details.html', {"form": form, 'object':livros})
    else:
        return redirect("login")




@login_required
def add_playlist(request, pk):
    livro = Ebook.objects.filter(id = pk) 
    if Playlist.objects.filter(livro = livro ).exists():
         messages.error(request,'Este livro ja foi adicionado na sua Playlist....')
         return HttpResponseRedirect(reverse('livro_details', args = pk))

    else:
        m, created = Playlist.objects.get_or_create( 
            livro_id = pk,
            user = request.user,
            adicionado = date.today(),
            )
        m.livro.set(m)
        m.save()
        messages.success(request,'O livro foi adicionado em sua Playlist com sucesso....')   

        return HttpResponseRedirect(reverse('livro_details', args = pk))

@login_required
def playlist(request): 
    playlists = Playlist.objects.filter(user = request.user)
    return render(request,'livros/playlist.html',{'playlists':playlists })

@login_required
def leitura(request):
    leituras = Leitura.objects.all()
    return render(request, 'livros/leitura.html',{'leituras':leituras})
    

@login_required
def add_leitura(request, id_livro):

    if Leitura.objects.filter(livro = id_livro ).exists():
        messages.success(request,'Este livro já está na sua lista de leitutra....') 
        return HttpResponseRedirect(reverse('livros:leitura'))

    else:
        ebook = Ebook.objects.filter(id = id_livro)
        for livro in ebook:
            livro       
        m, created = Leitura.objects.get_or_create( 
            
            livro_id = id_livro,
            titulo = livro.Title,
            user = request.user,            
            status = 0,
            inicio = date.today(),
            paginas = livro.Paginas,
            resenha = livro.Descricao,
            complete_per = 0,
            paginas_restante = 0

            )
      
               
        m.save()

        if Playlist.objects.filter(livro = id_livro ).exists():
            playlist = Playlist.objects.filter(livro = id_livro)
            playlist.delete()
            messages.success(request,'O livro foi adicionado em sua lista de leitura com sucesso....')  

        return HttpResponseRedirect(reverse('livros:leitura')) 


def leitura_details(request, pk):
    leitura = get_object_or_404(Leitura, id = pk)
    return render(request, 'livros/leitura_details.html',{'leitura':leitura })




@login_required
def iniciar_leitura(request, pk):
    leitura = Leitura.objects.get(id = pk)
    pre_requisitos = leitura.pre_requisitos.all()

    if len(pre_requisitos):
        for requisito in pre_requisitos:
            print(requisito.status)
            if requisito.status != '3':
                messages.info(request,'Este livro ainda não pode ser iniciado a leitura, pois você tem que terminar a leitura do ultimo livro.')
            else:
                leitura.inicio = datetime.now()
                leitura.save()
                leitura.iniciar()
    else:
        leitura.inicio = datetime.now()
        leitura.save()
        leitura.iniciar()
    return HttpResponseRedirect(reverse('livros:leitura_details', args=[pk]))


def pausar_leitura(request, pk):
    leitura = Leitura.objects.get(id = pk)
    leitura.pausar()
    return HttpResponseRedirect(reverse('livros:leitura_details', args=[ pk]))



def concluir_leitura(request, pk):    
    user = request.user
    leitura = Leitura.objects.get(id = pk)
    leitura.complete_per = 100    
    leitura.termino = datetime.now()
    leitura.paginas_restante = 0
    leitura.save()
    user.total_lidos += 1
    user.save()
    leitura.concluir()

    return HttpResponseRedirect(reverse('livros:leitura_details', args=[pk]))


def permissao_iniciar(request, pk):
    leitura = Leitura.objects.get(id = pk)
    return JsonResponse({"permitido": leitura.permitido_iniciar})


def paginas_conluida(request, pk ):
    leitura = Leitura.objects.get(id = pk) 
    livro = Leitura.objects.filter(id = pk)
    counter = 100 / leitura.paginas     
    leitura.paginas_restante += 1    
    leitura.complete_per = float(leitura.paginas_restante * counter)
    leitura.save()
    return HttpResponseRedirect(reverse('livros:leitura_details', args=[pk]))



def recomendacoes(request):
    return render(request, 'livros/recomendacoes.html')



def favoritos(request):
    favoritos = Favoritos.objects.filter(user = request.user)
    return render(request, 'livros/favoritos.html', {'favoritos':favoritos})


@login_required
def add_favoritos(request, livros_id):
    favoritos = Ebook.objects.filter(id = livros_id) 
    m, created = Favoritos.objects.get_or_create( 
            livro_id = livros_id,
            user = request.user,
            adicionado = date.today(),
            )
    
    m.save()
    return HttpResponseRedirect(reverse('index'))



def reviews(request):
    reviews = Review.objects.filter( user = request.user)
    return render(request, 'livros/reviews.html', {'reviews': reviews})


def discussoes(request):
    return render(request, 'livros/discussoes.html')