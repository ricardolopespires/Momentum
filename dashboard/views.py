from livros.views import leitura
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from livros.models import Ebook, Review, Leitura
from django.http import HttpResponseRedirect 
from django.db.models import F, Sum, Q 
from django.contrib import messages
from django.db.models import Avg
from datetime import date
from datetime import datetime
from accounts.models import User
from livros.models import Leitura





# Create your views here.




@login_required
def dashboard(request):
  reviews = Review.objects.all()
  reviews_avg = str(reviews.aggregate(Avg('rate'))['rate__avg'])
  user = request.user
  user.Average_Rating = reviews_avg[:3]
  user.Average_Count  = '0.' + reviews_avg.replace(',','.')[:1]
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

  return render(request, 'dashboard/index.html')