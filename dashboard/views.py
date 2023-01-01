
from django.views.generic import View, TemplateView, DetailView
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from livros.models import Ebook, Review, Leitura
from accounts.models import User, Experiencia
from django.http import HttpResponseRedirect 
from django.db.models import F, Sum, Q 
from django.contrib import messages
from livros.models import Leitura
from django.db.models import Avg
from datetime import datetime
from datetime import date


#from .recomentador import content_recommender, recommender_20

# Create your views here.




@login_required
def dashboard(request):


  if Review.objects.all().count() > 0:

    reviews = Review.objects.all()

    reviews_avg = reviews.aggregate(Avg('rate'))['rate__avg']

  else:
    reviews_avg = 0

 
  user = request.user
  user.Average_Rating = '{0:.1f}'.format(reviews_avg)
  user.Average_Count  = '{0:.1f}'.format(reviews_avg / 10)
  user.save()

  leituras = Leitura.objects.all()
  timeList = []

  for leitura in leituras:
    timeList.append('0'+ str(leitura.duracao_total))  

  totalSecs = 0
  for tm in timeList:
    tm = tm[:8]
    timeParts = [int(s) for s in tm.split(':')]
    totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]

  totalSecs, sec = divmod(totalSecs, 60)
  hr, min = divmod(totalSecs, 60)
  tempo = "%02d:%02d:%02d" % (hr, min, sec)
  user = request.user
  user.total_horas =tempo
  user.save()

  experiencias = Experiencia.objects.filter(Q(user = request.user.id),Q(is_active = True))


  return render(request, 'dashboard/index.html',{'experiencias':experiencias} )



# Create your views here.


class Lista_Livros_View(LoginRequiredMixin, View ):


  def get(self,request):

    livros = Ebook.objects.all()
    return render(request, 'dashboard/livros/list.html',{'livros':livros})



class Livro_Detial_View(LoginRequiredMixin,View):

  def get(self, request, livro_id):

    livro = get_object_or_404(Ebook, id = livro_id)

    livro.views += 1
    livro.save()

    reviews = Review.objects.filter(livro_id = livro.id )
    return render(request, 'dashboard/livros/detail.html',{'livro':livro, 'reviews':reviews})