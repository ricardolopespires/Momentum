from django import forms
from livros.models import Ebook, Capitulo, Review, Leitura





class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = [ 'titulo', 'descricao','publicacao','capa', 'poster', 'genero',
        'edicao','autor','editora','idioma', 'paginas','isbn',]



class Capitulo_Form(forms.ModelForm):

    class Meta:
        model = Capitulo
        fields = ['titulo','texto','pagina']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = []





class Leitura_Form(forms.ModelForm):

    class Meta:

        model = Leitura
        fields = ['duracao']


