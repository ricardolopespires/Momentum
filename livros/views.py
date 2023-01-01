from django.shortcuts import render, get_object_or_404, redirect
from .models import Ebook, Playlist, Review, Favoritos, Leitura, Quiz, Question, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EbookForm, Capitulo_Form, Leitura_Form
#from dashboard.recomentador import content_recommender
from django.db.models import Avg, Count, Sum ,F, Q
from datetime import datetime, date, timedelta
from .serializers import LivroListSerializer
from django.http import HttpResponseRedirect
from django.db.models import F, Sum, Q, Avg
from accounts.models import User, Answered
from livros.models import Ebook, Capitulo
from django.views.generic import View
from django.http import JsonResponse
from django.contrib import messages
from rest_framework import generics
from editora.models import Editora
from autor.models import Autor
from django.urls import reverse
from genero.models import Genero
from .core import porcentagem, data
from .forms import ReviewForm
from bs4 import BeautifulSoup
from decimal import Decimal
from uuid import uuid4
import datetime as dt, datetime
import statistics
import requests
import random
import json
import time
import lxml



@login_required
def livro_dashboard_details(request, livro_id):
    livro = get_object_or_404(Ebook, id = livro_id)
    leituras = Leitura.objects.filter(livro = livro)
    for leitura in leituras:
        livro.total_horas = leitura.duracao_total
        livro.views += 1
        livro.save()  

    return render(request, 'livros/livro_dashboard_details.html',{'livro':livro})



@login_required
def verificar(request):
    if request.method=='POST':
        titulo = request.POST.get("titulo")
        print(titulo)

        if Ebook.objects.filter(titulo = titulo).exists():
            messages.error(request,'Ops...., esse livro já foi adicionado, mais você pode ver a suas informações')
            return render(request, 'livros/verificar.html')

        else:
            messages.success(request, 'Escolha Opção que deseja para adicionar o novo livro, para nois adicionar no banco de dados')
            return HttpResponseRedirect(reverse('livros:opcao'))
    
    return render(request, 'livros/verificar.html')

 

class Opcao_Create_View(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'livros/opcao.html')




class Create_Amazon_View(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'livros/amazon.html')

    def post(self, request):

        if request.method == 'POST':

            url = request.POST.get('url')


            HEADERS = ({

                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
                'Accept-Language': 'en-US, en;q=0.5'

                })

            webpage = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "lxml")

            try:
                titulo = soup.find("span",attrs={"id": 'productTitle'}).string.strip().replace(',', '')
            except AttributeError:
                titulo = "NA"

            try:
                descricao = soup.find("div", id =( 'bookDescription_feature_div')).find('p').string.strip()
                #print(descricao) 
            except AttributeError:
                descricao = "NA"         

            try:
                preco = soup.find("span", attrs={'class': 'a-size-base a-color-secondary'}).string.strip().replace('R$', '')
                preco = float(preco[-5:].replace(',','.'))
                
            except AttributeError:
                preco = 0

            try:
                img = soup.find("img", class_=('frontImage'))['src']
            except AttributeError:
                img = "NA"

            try:
                paginas = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[1].find('span').string.strip()
                paginas = paginas[:-8]

                print(paginas)
            except AttributeError:
                paginas = 0

            try:
                idioma = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[1].find('span').string.strip()
            except AttributeError:
                idioma = "NA"

            try:
                editora = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[2].find('span').string.strip()
            except AttributeError:
                editora = "NA"

            try:
                publicacao = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[3].find('span').string.strip()
                
            except AttributeError:
                publicacao = "NA"

            try:
                isbn = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[6].find('span').string.strip()
            except AttributeError:
                isbn = "NA"  
            try:
                autor = soup.find("a", class_=('a-size-large a-link-normal')).find('h2').string.strip()
            except AttributeError:
                autor = "NA"


            codigo = url[-11:].replace('/','')

            if Ebook.objects.filter(id = codigo):
                messages.error(request, 'Este livro ja foi adicionado no banco de dados')
                return HttpResponseRedirect(reverse('livros:opcao'))

            else:


                m, created = Ebook.objects.get_or_create(

                    id = codigo,    
                    titulo = titulo,                    
                    descricao = descricao,
                    publicacao = data(publicacao),                
                    status =  'cadastrado',
                    popularidade = 0,
                    capa = img,
                    poster = img,                
                    edicao = 1,        
                    editora = editora,    
                    idioma = idioma,
                    paginas = int(paginas),
                    isbn = isbn,
                    classificacao = 0,                    
                    likes = 0,
                    horas = 0,
                    views = 0,
                    price = Decimal(preco),




                    )


            

            messages.success(request, 'O livro {} foi adicionado com sucesso'.format(titulo))
            return HttpResponseRedirect(reverse('dashboard:livro_detail', args = [codigo]))




class Create_zlibrary_View(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'livros/zlibrary.html')

    def post(self, request):

        if request.method == 'POST':

            url = request.POST.get('url')


            HEADERS = ({

                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
                'Accept-Language': 'en-US, en;q=0.5'

                })

            webpage = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "lxml")

            try:
                titulo = soup.find("span",attrs={"id": 'productTitle'}).string.strip().replace(',', '')
            except AttributeError:
                titulo = "NA"

            try:
                descricao = soup.find("div", id =( 'bookDescription_feature_div')).find('p').string.strip()
                #print(descricao) 
            except AttributeError:
                descricao = "NA"         

            try:
                preco = soup.find("span", attrs={'class': 'a-size-base a-color-secondary'}).string.strip().replace('R$', '')
                preco = float(preco[-5:].replace(',','.'))
                
            except AttributeError:
                preco = 0

            try:
                img = soup.find("img", class_=('frontImage'))['src']
            except AttributeError:
                img = "NA"

            try:
                paginas = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[1].find('span').string.strip()
                paginas = paginas[:-8]

                print(paginas)
            except AttributeError:
                paginas = 0

            try:
                idioma = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[1].find('span').string.strip()
            except AttributeError:
                idioma = "NA"

            try:
                editora = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[2].find('span').string.strip()
            except AttributeError:
                editora = "NA"

            try:
                publicacao = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[3].find('span').string.strip()
                
            except AttributeError:
                publicacao = "NA"

            try:
                isbn = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[6].find('span').string.strip()
            except AttributeError:
                isbn = "NA"  
            try:
                autor = soup.find("a", class_=('a-size-large a-link-normal')).find('h2').string.strip()
            except AttributeError:
                autor = "NA"


            codigo = url[-11:].replace('/','')

            if Ebook.objects.filter(id = codigo):
                messages.error(request, 'Este livro ja foi adicionado no banco de dados')
                return HttpResponseRedirect(reverse('livros:opcao'))

            else:


                m, created = Ebook.objects.get_or_create(

                    id = codigo,    
                    titulo = titulo,                    
                    descricao = descricao,
                    publicacao = data(publicacao),                
                    status =  'cadastrado',
                    popularidade = 0,
                    capa = img,
                    poster = img,                
                    edicao = 1,        
                    editora = editora,    
                    idioma = idioma,
                    paginas = int(paginas),
                    isbn = isbn,
                    classificacao = 0,                    
                    likes = 0,
                    horas = 0,
                    views = 0,
                    price = Decimal(preco),




                    )


            

            messages.success(request, 'O livro {} foi adicionado com sucesso'.format(titulo))
            return HttpResponseRedirect(reverse('dashboard:livro_detail', args = [codigo]))







@login_required    
def create_livro(request):
    generos = Genero.objects.all()
    autores = Autor.objects.all()
    editoras = Editora.objects.all()    
    codigo = str(uuid4())


    if request.method == "POST":        
        titulo = request.POST.get("titulo")      
        descricao = request.POST.get("descricao")
        publicacao = request.POST.get("publicacao")        
        capa = request.POST.get("capa")
        poster = request.POST.get("poster")
        generos = request.POST.getlist("genero")        
        edicao = request.POST.get('edicao')
        autores = request.POST.getlist("autor")      
        editora = request.POST.get("editora")
        idioma = request.POST.get("idioma")
        paginas = request.POST.get("Paginas")
        isbn = request.POST.get("isbn")

        livro = Ebook(

            id = isbn,    
            titulo = titulo,                    
            descricao = descricao,
            publicacao =publicacao,                
            status =  'cadastrado',            
            capa = capa,
            poster = poster,                
            edicao = edicao,
            editora_id = editora,              
            idioma = idioma,
            paginas = int(paginas),
            isbn = isbn,
            classificacao = 0,                    
            likes = 0,
            horas = 0,
            views = 0,
            preco = 0,

        )
        livro.save()
        
        if len(generos) > 0:
            for genre in generos:
                livro.genero.add(genre)

        if len(autores) > 0:    
            for author in autores:
                livro.autor.add(author)
            

        livro.user.add(request.user)

        request.user.livros.add(livro)
        request.user.Publicacoes += 1
        request.user.save()
        return HttpResponseRedirect(reverse('dashboard:manager'))


    else:
        return render(request, 'livros/created.html', { 

            'generos':generos,
            'autores':autores, 
            'editoras':editoras,

            })



def add_review(request, livro_id):

    if request.user.is_authenticated:
        print("O usário esta logado")
        username = get_object_or_404(User, name = request.user)
        print( username )
        livros = get_object_or_404(Ebook, id = livro_id)
        livro = Ebook.objects.get(id = livro_id) 

        rate = request.POST.get('rate')        

        if request.method == "POST":

            Review.objects.create(

                rate = rate,
                user =  username,
                livro_id = livro.id,

                )
        
        messages.success(

            request, 'Obrigado, {}, pela sua colaboaração e obrigado pela nota {} para o livro {} '.format(

                request.user, rate, livros

                )
            )   


        return HttpResponseRedirect(reverse('livro_details', args = [livro_id] )) 
    else:
        print('O usário não esta logado')
        return HttpResponseRedirect(reverse("login"))




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




class Leitura_List_View(LoginRequiredMixin, View):

    def get(self, request):
        leituras = Leitura.objects.filter(user_id = request.user.id )
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
            titulo = livro.titulo,
            user = request.user,            
            status = 0,
            inicio = date.today(),
            paginas = livro.paginas,
            resenha = livro.descricao,
            complete_per = 0,
            paginas_restante = 0

            )
      
               
        m.save()

        if Playlist.objects.filter(livro = id_livro ).exists():
            playlist = Playlist.objects.filter(livro = id_livro)
            playlist.delete()
            messages.success(request,'O livro foi adicionado em sua lista de leitura com sucesso....')  

        return HttpResponseRedirect(reverse('livros:leitura')) 


class Leitura_Detail_View(LoginRequiredMixin, View):

    def get(self, request, leitura_id):

         
        leitura = get_object_or_404(Leitura, id = leitura_id)

        livro = str( leitura.livro.titulo )
        #recomendacoes = content_recommender( livro )

        questoes = Quiz.objects.filter(livro_id = leitura.livro.id )

        
       
        return render(request, 'livros/leitura_details.html',{

            'leitura':leitura, 
            #'recomendacoes':recomendacoes,
            'questoes':questoes,        

            })




class Leitura_Pagina_View(LoginRequiredMixin, View):


    def get(self, request, leitura_id):

        leitura = get_object_or_404(Leitura, id = leitura_id)
        livro = get_object_or_404(Ebook, id = leitura.livro.id) 
        paginas = Capitulo.objects.filter( ebook_id = livro.id)

        return render(request, 'livros/leitura/index.html',{

            'livro':livro,
            'paginas':paginas,
            'leitura':leitura,

            })



#converte as palavras em minutos
def convert(text):
    total = 0
    
    for palavras in text.split():
        total += 1
    
    return timedelta(minutes = total/260)


#soma o total de minutos
def minutos(atual, novo):
    # transforma a string em data
    data_inicio = datetime.strptime(str(atual)[:7], "%H:%M:%S")

    horas, minutos, segundos = map(int, str(novo)[:7].split(':'))

    # transforma a string em timedelta
    duracao = timedelta(hours=horas, minutes=minutos, seconds=segundos)

    # soma a data à duração
    termino = data_inicio + duracao

    minutos = termino.strftime('%H:%M:%S')   

    # formata o resultado
    return timedelta(hours=int(minutos[:2]), minutes=int(minutos[::4]), seconds=int(minutos[:2]))




class Create_Pagina_View(LoginRequiredMixin, View):


    def get(self, request, leitura_id):
        form = Chapter_Form()
        leitura = get_object_or_404(Leitura, id = leitura_id)
        return render(request, 'livros/leitura/create.html',{'form':form, 'leitura':leitura})


    def post(self, request, leitura_id):

        codigo = str(uuid4())

        leitura = get_object_or_404(Leitura, id = leitura_id)

      
     
        order = Chapter.objects.filter(ebook_id = leitura.livro.id).count()

        if order > 0:

            order = order + 1
        else:
            order = 0

        
      


        if request.method == 'POST':

            form = Chapter_Form(request.POST)
            if form.is_valid():
                form.save(commit = False)
                titulo = form.cleaned_data['titulo']
                texto = form.cleaned_data['texto']
                paginas =form.cleaned_data['pagina']
                duracao = convert(texto)

              
                Chapter.objects.get_or_create(

                    id = codigo,
                    ebook_id = leitura.livro.id,
                    order = order,   
                    titulo = titulo,
                    texto = texto,
                    pagina = paginas,
                    leitura = False,
                    duracao = duracao,
                    )
              
            return HttpResponseRedirect(reverse('livros:leitura-paginas', args=[leitura_id])) 





class Pagina_leitura_View(LoginRequiredMixin, View):


    def get(self,request, pagina_id):

        pagina  = get_object_or_404(Chapter, id = pagina_id)
        leitura = get_object_or_404(Leitura, livro_id = pagina.ebook.id)

        return render(request, 'livros/leitura/pagina.html',{'pagina':pagina,'leitura':leitura})









'''
class Quiz_Data_View(LoginRequiredMixin, View):

    def get(self, request, leitura_id, questao_id):

        questoes = []       

        leitura = get_object_or_404(Leitura, id = leitura_id)
        questionario = get_object_or_404(Quiz, id = questao_id)

        quiz = Quiz.objects.get(id = questao_id)
        
        for q in quiz.get_questions():
            answers = []
            for a in q.get_answers():
                answers.append(a.text) 
            answer = answers.index(a.text)           

            questoes.append({'q':q.text,'options':answers,'answer':answer})


        quiz = json.dumps(questoes)

        print(quiz)


        return render(request, 'livros/questoes/index.html',{

            'leitura':leitura, 'quiz':quiz,

            })


'''
class Quiz_Data_View(LoginRequiredMixin, View):

    def get(self, request, leitura_id, questao_id):

        questoes = []

        leitura = get_object_or_404(Leitura, id = leitura_id)
        questionario = get_object_or_404(Quiz, id = questao_id)

        questoes = Question.objects.filter(Q(quiz_id = questionario.id), Q(answered = False ))
        perguntas = Answer.objects.all()

        #random.choice(Model.objects.all())
        
        return render(request, 'livros/questoes/index.html',{

            'leitura':leitura, 'questoes':questoes,
            'perguntas':perguntas, 'questionario':questionario,

            })



    def post(self, request,  leitura_id, questao_id):

        leitura = get_object_or_404(Leitura, id = leitura_id)
        questionario = get_object_or_404(Quiz, id = questao_id)
        
        total = 0
        

        if request.method == 'POST':

            respostas = request.POST.getlist('perguntas')
            
            for resposta in respostas:    

                for pergunta in Answer.objects.filter( text = resposta):
                    pergunta
                questao = get_object_or_404(Question, text = pergunta.question)
                if pergunta.correct == True:
                    #questao.answered = True
                    questao.save()
                    request.user.experiencia = request.user.experiencia + pergunta.punctuation
                    request.user.save()

                    
                    #Verificando a existencia da questão se já foi criada
                    if Answered.objects.filter(question_id = questao.id).exists():
                        pass

                    else:
                        #Gerando dados da questão que o usuário acertou
                        Answered.objects.get_or_create(

                            user_id = request.user.id,
                            livro_id = leitura.livro.id,
                            quiz_id = questionario.id,
                            question_id = questao.id,
                            topic = questionario.topic,
                            difficulty = questionario.difficulty,

                            )
                    
                    if total < 8:
                        total += 1

            quantidade = int(porcentagem(10, total))

            if total < 8:
                messages.error(request, 'Obs...; A porcetagem de acerto foi de {}% menor que o necessario'.format(quantidade))
            else:
                questionario.media = statistics.mean([total, 10])
                questionario.completed = True
                questionario.save()


                messages.success(request, 'Parabéns; A porcetagem de acerto foi de {}%. você alcançou a meta de Aprovação'.format(quantidade))

            return HttpResponseRedirect(reverse('livros:leitura_details', args = [leitura_id]))




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
    user.experiencia += 15
    user.save()
    leitura.concluir()

    return HttpResponseRedirect(reverse('livros:leitura_details', args=[pk]))


def permissao_iniciar(request, pk):
    leitura = Leitura.objects.get(id = pk)
    return JsonResponse({"permitido": leitura.permitido_iniciar})






def paginas_conluida(request, pagina_id):

    usuario = get_object_or_404(User, id = request.user.id)

    capitulo = get_object_or_404(Chapter, id = pagina_id)
    leitura = get_object_or_404(Leitura, livro_id = capitulo.ebook.id)

    tempo = minutos(leitura.duracao_total, capitulo.duracao)

    print(tempo)
    
    if leitura.paginas == leitura.paginas_restante:
        leitura.concluir()
        leitura.termino = datetime.now()
        leitura.save()
        leitura.duracao_total =  minutos()
        capitulo.leitura = True
        capitulo.save()
    else:

        counter = 100 / leitura.paginas     
        leitura.paginas_restante += capitulo.pagina    
        leitura.complete_per = float(leitura.paginas_restante * counter)
        leitura.duracao_total =  minutos()            
        leitura.save()        
        
        capitulo.leitura = True
        capitulo.save()

    

    return HttpResponseRedirect(reverse('livros:leitura-paginas', args=[leitura.id]))



class Questoes_Ebook_View(LoginRequiredMixin, View):


    def get(self, request,):       
       

        return render(request,'livros/questoes/index.html')


    def post(self, request, leitura_id):

        
        
        if request.method == 'POST':

            respostas = request.POST.getlist('respostas')

            print(respostas)

           



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