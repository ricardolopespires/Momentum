from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from livros.models import Leitura
from genero.models import Genero
from .models import User

# Create your views here.





def loggin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                if user.groups.filter(name='Administrador').exists() == True:
                    login(request,user)
                    #Redirect to success page.
                    form = LoginForm()                
                    return redirect('management:index')
                else:
                    login(request,user)
                    #Redirect to success page.
                    form = LoginForm()                
                    return redirect('dashboard:manager')
                    

    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'registration/registro.html',{'form':form})

   
def profile_users(request):
    profiles = User.objects.all()    
    leituras = Leitura.objects.filter(user_id = request.user.id)
    categorias = Genero.objects.filter(usuarios = request.user.id )

    

   
    return render(request, 'profile/index.html',{

        'profiles':profiles,
        'leituras':leituras,
        'categorias':categorias,

        })


def profile_details(request, pk):
    user_profile = get_object_or_404(User, id = pk)     

    return render(request, 'profile/details.html',{'user_profile':user_profile, })