from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Sum ,F, Q
from django.views.generic import View
from django.shortcuts import render

# Create your views here.






class Analytics(LoginRequiredMixin, View):

	def get(self, request):
		return render(request, 'analytics/index.html')
