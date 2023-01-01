from django.views.generic import View, TemplateView, DetailView
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from livros.models import Ebook, Review, Leitura, Quiz, Question
from django.http import HttpResponseRedirect 
from django.db.models import F, Sum, Q
from django.shortcuts import render
from django.contrib import messages

# Create your views here.





from datetime import datetime

day = datetime.now().day
month = datetime.now().month
year = datetime.now().year 






class Management_View(LoginRequiredMixin, View):

	def get(self, request):

		#-------------------------- Livros --------------------------------------------------------------

		#Buscando os dados por mes e ano
		livros = Ebook.objects.filter(Q(Created__month = month), Q(Created__year = year))

		#Buscando os dados pelo dia de hoje
		ultimos = Ebook.objects.filter(Q(Created__day = day ),Q(Created__month = month), Q(Created__year = year))

		#O total de livros
		total_livros = livros.count()

		pendentes = livros.filter(status__startswith = 'pendentes').count()

		cadastrados = livros.filter(status__startswith = 'cadastrado').count()

		cancelado = livros.filter(status__startswith = 'cancelado').count()


		print(month)




		#-------------------------- Livros --------------------------------------------------------------



		#-------------------------- Livros --------------------------------------------------------------



		return render(request, 'management/manager/index.html',{

			'ultimos':ultimos,
			'month':month,
			'total_livros':total_livros,
			'pendentes':pendentes,
			'cadastrados':cadastrados,
			'cancelado':cancelado,



			})



class Lista_Livros_View(LoginRequiredMixin, View ):


  def get(self,request):

    livros = Ebook.objects.all()
    return render(request, 'management/manager/livros/list.html',{'livros':livros})





class Livro_Detial_View(LoginRequiredMixin,View):

  def get(self, request, livro_id):

    livro = get_object_or_404(Ebook, id = livro_id)

   

    livros = Ebook.objects.filter(id = livro_id)


    reviews = Review.objects.filter(livro_id = livro.id )

    questionarios = Quiz.objects.filter(livro_id = livro_id) 

    total_leitor = Leitura.objects.filter(livro_id = livro.id).count
    
    total_lendo = Leitura.objects.filter(Q(livro_id = livro.id),Q( lendo = True)).count

    total_litura_concluida = Leitura.objects.filter(Q(livro_id = livro.id),Q( concluido= True)).count

    return render(request, 'management/manager/livros/detail.html',{

    	'livro':livro, 'reviews':reviews,
    	'questionarios': questionarios,
    	'total_leitor':total_leitor,
    	'total_lendo':total_lendo,
    	'total_litura_concluida':total_litura_concluida,


    	})



class Created_Quiz_View(LoginRequiredMixin, View):


	def get(self, request, livro_id):

		livro = get_object_or_404(Ebook, id = livro_id)
		livros = Ebook.objects.all()

		return render(request, 'management/manager/form/created.html', {'livro':livro, 'livros':livros,})


	def post(self, request, livro_id):
		

		if request.method == 'POST':

			livros = get_object_or_404(Ebook, id = livro_id)

			name = request.POST.get('name')
			livro = request.POST.get('livro')
			topic = request.POST.get('topic')
			number_of_questions = request.POST.get('number_of_questions')
			time = request.POST.get('time')
			required_score_to_pass = request.POST.get('required_score_to_pass')
			difficulty = request.POST.get('difficulty')
			status = request.POST.get('status')
			media = request.POST.get('media')
			completed = request.POST.get('completed')


			if Quiz.objects.filter(name = name).exists():

				messages.error(request, 'O questionário '+str(name)+' Já foi criado')

				return HttpResponseRedirect(reverse('management:livro_detail', args =[livro_id]))

			else:

				Quiz.objects.get_or_create(

				id   = livro,	
				name = name,
				livro_id = livro,
				topic = topic,
				number_of_questions = number_of_questions,
				time = time,
				required_score_to_pass = required_score_to_pass,
				difficulty = difficulty,
				status   = status,
				media = media,
				completed = completed,

				)

			messages.success(request, 'O questionáriodo livro '+str( livros )+' foi criado com sucesso')
			return HttpResponseRedirect(reverse('management:livro_detail', args =[livro_id]))