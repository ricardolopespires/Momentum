from .serializers import LivroListSerializer
from django.views.generic import  View
from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render
from .models import Ebook
# Crie suas visualizações aqui.

#Crie suas visualizações aqui













class LivroListAPIView(generics.ListAPIView):
    queryset = Ebook.objects.all()
    serializer_class = LivroListSerializer
