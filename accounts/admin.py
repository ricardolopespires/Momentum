from django.contrib import admin
from .models import User, Newsletter

# Registre suas modelos aqui.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name','date_of_birth']


@admin.register(Newsletter)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'email']
