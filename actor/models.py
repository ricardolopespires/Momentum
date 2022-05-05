from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Actor(models.Model):	
	name = models.CharField(max_length=150, unique=True)
	picture = models.URLField()
	slug = models.SlugField(null=True, unique=False)
	movies = models.ManyToManyField('movie.Movie', related_name= 'actors_movies')
	
	def get_absolute_url(self):
		return reverse('actors', args=[self.slug])

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		return super().save(*args, **kwargs)
