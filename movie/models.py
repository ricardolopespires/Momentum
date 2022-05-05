from django.db import models
from actor.models import Actor
from  genre.models import Genre
from director.models import Director
from django.utils.text import slugify
import requests
from io import BytesIO
from django.core import files
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField 
from multiselectfield import MultiSelectField
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Rating(models.Model):
	source = models.CharField(max_length=50)
	rating = models.CharField(max_length=10)

	def __str__(self):
		return self.source


class Movie(models.Model):

	STATUS_CHOICES = (
                        ('cartaz','Cartaz'),
                        ('em breve','Em Breve'),
                        ('lançamento','Lançamento'),
                        ('geral', 'Geral'),
                        ('novo','Novo')
                      )
	id = models.IntegerField(primary_key = True, )
	user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'usename', blank=True)
	Title = models.CharField(max_length=200)
	Year = models.DateTimeField(auto_now_add=True,  blank=True) 
	Publish = models.DateTimeField(default=timezone.now,  blank=True)
	Created = models.DateTimeField(auto_now_add=True,  blank=True) 
	Updated = models.DateTimeField(auto_now=True,  blank=True)
	Status = models.CharField(max_length = 140, choices = STATUS_CHOICES , default = 'geral',  blank=True)  
	Popularity = models.IntegerField()
	Released = models.DateTimeField(auto_now_add=True,  blank=True) 
	Runtime = models.CharField(max_length=25, blank=True)
	Genre = models.ManyToManyField(Genre, blank=True)	
	Actors = models.ManyToManyField(Actor, blank=True)
	Directors =  models.ManyToManyField(Director, blank=True)
	Description = models.CharField(max_length=900, blank=True)
	Language = models.CharField(max_length=300, blank=True)
	Country = models.CharField(max_length=100, blank=True)
	Awards = models.CharField(max_length=250, blank=True)
	Poster = models.URLField(blank=True)
	Poster_url = models.URLField(blank=True)
	Ratings = models.ManyToManyField(Rating, blank=True)			
	Average_Rating = models.CharField(max_length=5, blank=True)
	Average_Count = models.CharField(max_length=100, blank=True)
	Votes_Count = models.CharField(max_length=100, blank=True)
	Budget = models.IntegerField(default=0,  blank=True)
	Revenue = models.IntegerField(default=0,  blank=True)
	imdbID = models.CharField(max_length=100, blank=True)	
	Filmes_views = models.IntegerField(default=0,  blank=True)
	Video = models.IntegerField(default=0,  blank=True)
	Trailler = models.CharField(max_length=100, blank=True, null = True)
	Watched = models.IntegerField( default=0,  blank=True)  
	Type = models.CharField(max_length=100, blank=True)
	
	
	def __str__(self):
		return self.Title


	def persona(self):

		self.persona = self.Filmes_views + self.Watched
		return self.persona

	def porcetagem_views(self):
		porcetagem_views = self.Filmes_views *0.1
		return porcetagem_views


	def porcetagem_Watched(self):
		porcetagem_Watched = self.Watched 
		return porcetagem_Watched


	def save(self, *args, **kwargs):
		if self.Poster == '' and self.Poster_url !='':
			resp = requests.get(self.Poster_url)
			pb = BytesIO()
			pb.write(resp.content)
			pb.flush()
			file_name = self.Poster_url.split("/")[-1]
			self.Poster.save(file_name, files.File(pb), save=False)

		return super().save(*args, **kwargs)

	def __str__(self):
		return self.Title

	def save(self, *args, **kwargs):
		if self.Poster == '' and self.Poster_url !='':
			resp = requests.get(self.Poster_url)
			pb = BytesIO()
			pb.write(resp.content)
			pb.flush()
			file_name = self.Poster_url.split("/")[-1]
			self.Poster.save(file_name, files.File(pb), save=False)

		return super().save(*args, **kwargs)


class Trailler(models.Model):
	id = models.CharField(max_length = 150, primary_key = True )
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'user_movie_trailler', on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)	



class Review(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'user_movie_review', on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)	
	rate = models.DecimalField(max_digits=10,decimal_places=2)
	media = models.CharField(max_length = 10)
	
	def __str__(self):
		return self.user.username

class Like(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name='user_movie_like')
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	number = models.PositiveSmallIntegerField()
	
