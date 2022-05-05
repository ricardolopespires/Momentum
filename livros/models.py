from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.db.models.fields import URLField
from genre.models import Genre
from author.models import Author
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

    

class Ebook(models.Model):
    id = models.CharField(max_length = 150, primary_key = True)    
    Title = models.CharField(max_length = 150,)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'user', blank=True)
    Descricao = models.TextField()
    Publish = models.DateTimeField(auto_now_add =False,  blank=True)
    Created = models.DateTimeField(auto_now_add=True,  blank=True) 
    Updated = models.DateTimeField(auto_now=True,  blank=True)
    Popularity = models.IntegerField(default=0)
    Poster = models.URLField(blank=True)
    Poster_url = models.URLField(blank=True)
    Genero = models.ManyToManyField(Genre, blank=True)
    Edicao = models.IntegerField()
    Autor = models.ManyToManyField(Author, blank = True) 
    Editora = models.CharField(max_length=150, blank = True)    
    Linguagem = models.CharField(max_length = 150, blank = True)
    Paginas = models.IntegerField()
    ISBN = models.CharField( max_length = 90)
    Average_Rating = models.CharField(max_length=5, blank=True, default = 0)
    Average_Count = models.CharField(max_length=100, blank=True, default = 0)
    Votes_Count = models.CharField(max_length=100, blank=True, default = 0)
    Likes = models.IntegerField(blank = True, null = True, default = 0)
    total_horas = models.CharField(max_length=150, default = '00:00:00')
    

    def __str__(self):
        return self.Title


 

class Review(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'user_livro_review', on_delete=models.CASCADE)
	livro = models.ForeignKey(Ebook, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)	
	rate = models.IntegerField()
	
	
	def __str__(self):
		return self.user.username





class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name='user_livro_like')
    livro = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()


    def __str__(self):
        return self.livro


class Favoritos(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='user_favoritos')
    livro = models.ForeignKey(Ebook, on_delete=models.CASCADE, related_name='favoritos')
    adicionado = models.DateTimeField(auto_now_add = True, blank=True, null=True)

    



class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user_playlist')
    titulo = models.CharField(max_length = 150, unique = True)
    img = URLField()
    livro = models.ManyToManyField(Ebook)
    adicionado = models.DateTimeField(auto_now_add = True, blank=True, null=True)

    def __str__(self):
        return self.titulo


 
class Leitura(models.Model):

    STATUS_DA_LEITURA = (
        (0, "PROJETO"),
        (1, "LENDO"),
        (2, "PAUSADA"),
        (3, "CONCLUíDA")
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user_leitura')
    titulo = models.CharField(max_length = 150, blank=True, null=True)
    livro = models.ForeignKey(Ebook, related_name = 'livro', on_delete = models.CASCADE)
    status = models.CharField(max_length = 40, default = 0, choices = STATUS_DA_LEITURA )
    inicio = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    termino = models.DateTimeField(null=True, blank = True)
    duracao_total = models.DurationField( null=True,  default=timedelta(seconds=0))
    paginas = models.IntegerField(default=0)
    paginas_restante = models.IntegerField(default=0)
    resenha = models.TextField(blank = True, null = True)
    complete_per = models.IntegerField( validators = [MinValueValidator(0), MaxValueValidator(100)], default=0)
    pre_requisito = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="pre_requisitos", 
    )

    class Meta:
        odering = ['-inicio']
        verbose_name = 'livro'
        verbose_name_plural = 'livros'

    def __str__(self):
        return self.livro



    @property
    def is_open(self):
        return self.status == '0'

    @property
    def is_running(self):
        return self.status == '1'

    @property
    def is_paused(self):
        return self.status == '2'

    @property
    def is_done(self):
        return self.status == '3'

    def iniciar(self):
        self.inicio  = timezone.now()
        self.status = 1

        self.save()

    def concluir(self):

        self.dataconclusao = timezone.now()
        self.duracao_total += timezone.now() - self.dataconclusao
        self.status = 3
        self.save()

    def pausar(self):
        diferenca = timezone.now() - self.inicio 
        self.duracao_total += diferenca
        self.status = 2
        self.save()

    @property
    def permitido_iniciar(self):

        for requisito in self.pre_requisitos:
            if requisito.status != 3:
                return False
        return True

    class Meta:
        db_table = "leitura"

    def __str__(self):
        return "{}, {}".format(self.titulo, self.status)
