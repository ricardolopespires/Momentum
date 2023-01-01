from django.urls import path
from . import views



app_name = 'analytics'




urlpatterns = [

	path('analytics/',views.Analytics.as_view(), name = 'index'),



]