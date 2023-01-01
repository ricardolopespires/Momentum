from django.db import models

# Create your models here.


class Categoria(models.Model):	
	titulo =  models.CharField(max_length = 150, help_text = "O titulo da categoria prestação de serviço")
	slug = models.SlugField()
	descricao = models.TextField(help_text = 'A descricição da categoria', blank = True)
	quantidade = models.IntegerField(help_text = 'A quantidade de livros nesta categoria', default = 0 )
	ranking = models.IntegerField(help_text = 'A Classificação que esta a categoria', default = 0 )
	popularidade = models.IntegerField(help_text = "A Popularidade da categoria ", default = 0 )
	is_active = models.BooleanField(default = False, help_text = 'se tem genero cadastrado')
	icone =  models.CharField(max_length = 150, help_text = 'icone', default = 'fas fa-book-reader')


	class Meta:
		verbose_name = "Categoria"
		verbose_name_plural = "Categorias"



	def __str__(self):
		return self.titulo



class Genero(models.Model):	
	titulo = models.CharField(max_length=150)	
	categoria = models.ForeignKey(Categoria, related_name = "categorias",  on_delete = models.CASCADE)
	slug = models.SlugField(null=False, unique=False)	
	descricao = models.TextField(help_text = 'A descricição da categoria', blank = True, null = True)
	quantidade = models.IntegerField(help_text = 'A quantidade de livros deste genero', default = 0 )
	ranking = models.IntegerField(help_text = 'A Classificação que esta esse genero', default = 0 )
	popularidade = models.IntegerField(help_text = "A Popularidade deste genero ", default = 0 )
	livros = models.ManyToManyField('livros.Ebook', related_name= 'genero_livros', blank=True)
	usuarios = models.ManyToManyField('accounts.User', related_name= 'categorias', blank=True)
	


	class Meta:

		verbose_name = "Genero"
		verbose_name_plural = "Generos"


	def get_absolute_url(self):
		return reverse('genres', args=[self.slug])


	def __str__(self):
		return self.titulo

	def save(self, *args, **kwargs):
		if not self.slug:
			self.tituloreplace(" ", "")
			self.slug = slugify(self.titulo)
		return super().save(*args, **kwargs)
