from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Newsletter
User = get_user_model()




class LoginForm(forms.Form):
    username = forms.CharField(max_length = 190 )
    password = forms.CharField( widget=forms.PasswordInput)



class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField( widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Comfirme seu Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username = username)
        if qs.exists():
            raise forms.ValidationError('Nome de usuário está Registrado')
        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email = email)
        if qs.exists():
            raise forms.ValidationError('email de usuário está Registrado')
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("A senha estão diferentes.")
        return data




class NewsletterForm(forms.ModelForm):


    class Meta:
        model = Newsletter
        fields = ('__all__')