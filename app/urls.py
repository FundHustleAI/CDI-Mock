from django.urls import path
from . import views

urlpatterns = [
     path('', views.auth_screen, name='auth'),  # Login/register screen
    path('home/', views.home, name='home'),  # Home screen with categories
    path('instructions/', views.instructions, name='instructions'),  # Instructions screen
    path('start-test/<str:category>/', views.start_test, name='start_test'),  # Start a specific test
    path('logout/', views.logout_view, name='logout'),  # Logout
]
