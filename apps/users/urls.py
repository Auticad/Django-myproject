"""URL utenti — apps/users/urls.py"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',  views.SignUpView.as_view(),         name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(),  name='profile'),
]
