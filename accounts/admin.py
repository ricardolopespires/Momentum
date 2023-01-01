from django.contrib import admin
from .models import User, Newsletter, Answered, Experiencia

# Registre suas modelos aqui.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name','date_of_birth','experiencia']


@admin.register(Newsletter)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'email']



@admin.register(Answered)
class UserAdmin(admin.ModelAdmin):
    list_display = ['quiz','question']



@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ['nivel','pontuacao','porcentagem','total','is_active']