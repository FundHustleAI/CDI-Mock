from django.urls import path
from .views import home, auth_screen

urlpatterns = [
    path('', home, name='home'),
    path('auth/', auth_screen, name='auth'),
]
