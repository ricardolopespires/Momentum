from django import forms
from livros.models import Ebook, Review





class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = [ 'Title', 'Descricao','Publish','Poster', 'Poster_url', 'Genero',
        'Edicao','Autor','Editora','Linguagem', 'Paginas','ISBN',]





class ReviewForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = []