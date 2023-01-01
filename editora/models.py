from django.db import models

# Create your models here.
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db import models
# Create your models here.

class Editora(models.Model):


	STATUS_IDIOMA = (

            ('português','Português'),
            ('inglês','Inglês'),
            ('espanhol','Espanhol'),
            ('italiano','Italiano'),
            ('francês','Francês'),
            ('alemão','Alemão'),
            ('catalão','Catalão'),

        )

	id = models.CharField(max_length = 150, primary_key = True) 
	nome = models.CharField(max_length=70, unique=True)
	logo = models.URLField(blank = True, null = True)
	slug = models.SlugField(null=True, unique=False)
	descricao = RichTextField(blank = True, null = True)
	idioma = models.CharField(max_length = 150, choices = STATUS_IDIOMA, default = 'inglês')
	livros = models.ManyToManyField('livros.Ebook', related_name= 'editora_ebook', blank = True)	

	

	def __str__(self):
		return self.nome

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		return super().save(*args, **kwargs)
