from django.shortcuts import render
from .models import Author
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.








def verificar(request):
    if request.method=='POST':
        nome = request.POST.get("nome")
        print(nome)

        if Author.objects.filter(name = nome).exists():
            messages.error(request,'Ops...., esse autor já foi adicionado, mais você pode ver a suas informações')
            return render(request, 'livros/verificar.html')

        else:
            messages.success(request, 'Legal esse autro ainda não foi adicionado, vamos adicionar')
            return HttpResponseRedirect(reverse('author:adicionar'))
    
    return render(request, 'author/verificar.html')




def created(request):
    if request.method == 'POST':
        nome = request.POST.get("nome")      
        url = request.POST.get("url")
        slug = request.POST.get("slug")
        author = Author(

            name = nome,
            picture = url,
            slug = slug,
                )
        author.save()
        return HttpResponseRedirect(reverse('dashboard:manager'))

    return render(request, 'author/created.html')