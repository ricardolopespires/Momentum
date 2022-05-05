from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Author(models.Model):	
	name = models.CharField(max_length=70, unique=True)
	picture = models.URLField()
	slug = models.SlugField(null=True, unique=False)
	#livro = models.ManyToManyField('ebook.Ebook', related_name= 'actors_ebook')	

	

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		return super().save(*args, **kwargs)
