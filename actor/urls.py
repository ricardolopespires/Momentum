from django.urls import path
from actor.views import actors


app_name = 'actor'



urlpatterns = [
	path('<slug:actor_slug>', actors, name='actors'),
]