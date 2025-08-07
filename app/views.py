from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User

def auth_screen(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')

        if username and phone_number:
            user = User.objects.filter(username=username, phone_number=phone_number).first()
            if user:
                login(request, user)
                return redirect('home')
            else:
                # create user
                user = User.objects.create_user(username=username, phone_number=phone_number)
                login(request, user)
                return redirect('home')
        else:
            error = "Both fields are required."

    return render(request, 'auth.html', {'error': error})



def home(request):
    return render(request, 'home.html')