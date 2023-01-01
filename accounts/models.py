from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.core.validators import MaxValueValidator, MinValueValidator
from livros.models import Ebook, Quiz, Question
from ckeditor.fields import RichTextField
#from dashboard.views import reviews
from phone_field import PhoneField
from django.core import validators
from django.utils import timezone 
from django.conf import settings
#from movie.models import Movie
from datetime import timedelta
from livros.models import Ebook
from django.db import models
import re
# Create your models here.



class User(AbstractBaseUser, PermissionsMixin):

    STATUS_GENRE = (
                    ('masculino', 'Masculino'),
                    ('feminino','Feminino')
                    )

    STATUS_CHOICES = (
                        ('ativos','Ativos'),
                        ('pendentes','Pendentes'),
                        ('inativos','Inativos'),
                     )

    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True, 
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
            'O nome de usuário só pode conter letras, digitos ou os '
            'seguintes caracteres: @/./+/-/_', 'invalid')]
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    address = models.CharField('Endereço', max_length = 190, blank = True)
    date_of_birth = models.DateTimeField(default=timezone.now) 
    state = models.CharField('Estado',  max_length = 100, blank = True)
    status = models.CharField(max_length = 100, choices = STATUS_CHOICES, default = 'ativos')
    genre = models.CharField(max_length = 100, choices = STATUS_GENRE, default = 'masculino')
    city = models.CharField('Cidade', max_length = 190, blank = True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)
    img = models.ImageField(upload_to = 'user', blank = True)
    livros = models.ManyToManyField(Ebook, related_name= 'user_livros', blank = True)
    #leitura = models.ManyToManyField(Leitura, related_name = 'leitura_user_livros', blank = True)
    #favoritos = models.ManyToManyField(Favoritos, related_name = 'favoritos_user_livros', blank = True)
    #playlist =  models.ManyToManyField(Playlist, related_name = 'playlist_user_livros', blank = True)
    #reviews = models.ManyToManyField(Favoritos, related_name = 'reviews_user_livros', blank = True)
    #movie = models.ManyToManyField(Movie, related_name = 'user_movie', blank=True )
    total_horas = models.CharField(max_length = 50, default = "00:00:00")
    total_lidos = models.IntegerField('O tota de livros já lidos',  default=0)
    Average_Rating = models.CharField(max_length=4, default = 0)
    Average_Count = models.CharField(max_length=4, default = 0, blank=True)
    Publicacoes = models.IntegerField(default=0)
    experiencia = models.IntegerField(default = 0 , help_text = "O Total de experiência do conhecimento ")
 

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets', on_delete = models.CASCADE
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']




class Newsletter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário_newsletter',
       related_name='usuário_newsletter', on_delete = models.CASCADE, blank = True, null = True )
    email = models.EmailField()

    def __str__(self):
        return self.email





class Answered(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        related_name='usuário_answered', on_delete = models.CASCADE, blank = True, null = True )
    livro = models.ForeignKey(Ebook, related_name = 'livro_answered', on_delete = models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name = 'quiz_answered', on_delete = models.CASCADE)
    question = models.ForeignKey(Question, related_name = 'question_answered', on_delete = models.CASCADE)
    topic = models.CharField(max_length = 120)
    difficulty = models.CharField(max_length = 9)
    created = models.DateTimeField(auto_now_add = True)


    class Meta:
        verbose_name = 'Questão Resolvida'
        verbose_name_plural = 'Questões Resolvidas'
        

    def __str__(self):
        return f'{self.livro}, {self.quiz}, {self.question}'




class Experiencia(models.Model):
    nivel = models.IntegerField(default = 0)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'experiências', blank=True)    
    porcentagem = models.IntegerField(help_text = 'Porcetagem da Experiência', default = 0)
    pontuacao = models.IntegerField(help_text = 'Pontuação da Experiência', default = 0)
    total = models.IntegerField(help_text = 'total da Experiência do nivel', default = 0)
    is_active = models.BooleanField( default = False)



    def save(self, *args, **kwargs):

        porcentagem = 100
        try:
            calculo = porcentagem / self.total
        except ZeroDivisionError:
            calculo = porcentagem / 1
        resultado = self.pontuacao * calculo
        self.porcentagem =  float("{0:.2f}".format(resultado))       

        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Experiência'
        verbose_name_plural = 'Experiências'


    def __str__(self):
        return f'{self.nivel}, {self.porcentagem}'  



class habilidades(models.Model):    
    titulo = models.CharField(max_length = 450,)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'habilidades', blank=True)
    descricao = RichTextField(blank = True, null = True)
    porcetagem = models.IntegerField(help_text = 'Porcetagem da habilidades', default = 0)


    class Meta:
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'
        

    def __str__(self):
        return f'{self.titulo}, {self.porcetagem}'   