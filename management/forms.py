from django import forms
from livros.models import Quiz





class QuizForm(forms.ModelForm):


	class Meta:
		model = Quiz
		fields = ('__all__')