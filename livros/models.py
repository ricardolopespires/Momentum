from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import URLField
from ckeditor.fields import RichTextField
from editora.models import Editora
from django.utils import timezone
from django.conf import settings
from genero.models import Genero
from autor.models import Autor
from datetime import timedelta
from django.db import models
import uuid

# Create your models here.

    

class Ebook(models.Model):

    STATUS_CHOICES = (

        ('pendentes','pendentes'),
        ('cadastrado','cadastrado'),
        ('cancelado','cancelado')

        )

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
    titulo = models.CharField(max_length = 450,)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'user', blank=True)
    descricao = RichTextField(blank = True, null = True)
    publicacao = models.DateTimeField(auto_now_add =False,  blank=True, null = True)
    created = models.DateTimeField(auto_now_add=True,  blank=True) 
    updated = models.DateTimeField(auto_now=True,  blank=True)
    status = models.CharField(max_length = 14, choices = STATUS_CHOICES, default = 'pendentes')   
    capa= models.URLField(blank=True, null = True)
    poster = models.URLField(blank=True, null = True)
    genero = models.ManyToManyField(Genero, blank=True)
    edicao = models.IntegerField()
    autor = models.ManyToManyField(Autor, blank = True,) 
    editora = models.ForeignKey(Editora, related_name = 'editora_ebook', on_delete = models.CASCADE)    
    idioma = models.CharField(max_length = 150, choices = STATUS_IDIOMA, default = 'inglês')
    paginas = models.IntegerField()
    isbn = models.CharField( max_length = 90)
    classificacao = models.CharField(max_length =  3, blank = True )
    average_rating = models.CharField(max_length=5, blank=True)
    average_count = models.CharField(max_length=100, blank=True)    
    likes = models.IntegerField(blank = True, null = True, default = 0)
    horas = models.CharField(max_length=150, default = '00:00:00')
    views = models.IntegerField(default=0 , help_text = 'O total de visualizações')
    preco = models.DecimalField(decimal_places = 2, max_digits = 4, help_text = 'O preço do livro')
    

    def __str__(self):
        return self.titulo



class Capitulo(models.Model):
    id = models.CharField(max_length = 150, primary_key = True)
    ebook = models.ForeignKey(Ebook, related_name = 'chapter_ebook', on_delete = models.CASCADE)
    order = models.IntegerField(default = 0)    
    titulo = models.CharField(max_length = 700, )
    texto = RichTextField(help_text = 'O conteudo do texto do livro')
    pagina = models.IntegerField(default = 0)
    leitura = models.BooleanField(default = False, help_text = 'O capitulo já foi lido')   
    duracao = models.DurationField( null=True,  default=timedelta(seconds=0))




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
    lendo = models.BooleanField(default = False, help_text = 'O leitor está lendo o livro ')
    concluido = models.BooleanField(default = False, help_text = 'O leitor concluiu a leitura do livro ')
    duracao = models.DurationField( null=True,  default=timedelta(seconds=0))
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





class Livros_Analytics(models.Model):
    id = models.CharField(max_length = 150, primary_key = True)    
    title = models.CharField(max_length = 450,)   
    descricao = RichTextField(blank = True, null = True)
    publish = models.DateTimeField(auto_now_add =False,  blank=True)
    popularity = models.IntegerField(default=0)
    poster = models.URLField(blank=True)
    poster_url = models.URLField(blank=True)
    genero = models.CharField(max_length = 400,  blank=True, null = True)
    edicao = models.IntegerField()
    autor  = models.CharField(max_length = 400,  blank=True, null = True) 
    editora = models.CharField(max_length=150, blank = True)    
    linguagem = models.CharField(max_length = 150, blank = True)
    paginas = models.IntegerField()
    isbn = models.CharField( max_length = 90)
    average_rating = models.CharField(max_length =  3, blank = True )
    average_count = models.CharField(max_length =  3, blank = True )
    votes_count = models.IntegerField( default = 0)
    likes = models.IntegerField(blank = True, null = True, default = 0)
    total_horas = models.CharField(max_length=150, default = '00:00:00')
    

    class Meta:

        ordering = ['-publish']
        verbose_name = 'Analise de livro'
        verbose_name_plural = 'Analise de livros'


    def __str__(self):
        return f'{self.title}'


        





class Quiz(models.Model):



    STATUS_CHOICES = (

            ('projeto', 'projeto'),
            ('elaboração','elaboração'),
            ('concluido','concluido')



        )



    DIFF_CHOICES = (


            ('fácil', 'fácil'),
            ('medium', 'medium'),
            ('dificil', 'dificil'),

        )



    id = models.CharField(max_length = 110, primary_key = True)
    name = models.CharField(max_length = 120)
    livro = models.ForeignKey(Ebook, related_name = 'quiz_livro', on_delete = models.CASCADE)
    topic = models.CharField(max_length = 120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text = "duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text = "required score in %")
    difficulty = models.CharField(max_length = 9, choices=DIFF_CHOICES)
    status = models.CharField(max_length = 14, choices = STATUS_CHOICES , default = 'projeto', help_text = 'O status do questionário')
    media = models.IntegerField(default = 0)
    completed = models.BooleanField(default = False, null = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        return self.question_set.all()

    class Meta:
        verbose_name_plural = 'Quizes'




class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default = False)



    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    punctuation = models.IntegerField(default= 0 )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"




class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user_result')
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)