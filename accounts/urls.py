from django.contrib.auth import views as auth_views
from django.urls import path
from . import views



urlpatterns = [

    path('login/',views.loggin, name = 'login'),
    path('register/',views.register, name = 'register'),
    path('logout/',auth_views.LogoutView.as_view(), name = 'logout'), 



    #---------------------------------- Settings  profile ----------------------------
    path('profile/user/settings/',views.profile_users, name = 'profile'), 
    path('profile/user/<int:pk>/detials/', views.profile_details, name = 'details'),     
    path('profile/user/settings/',views.profile_users, name = 'profile'),

  
]



