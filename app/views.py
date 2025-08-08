import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Test, User, UserProgress


def auth_screen(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')

        if username and phone_number:
            user = User.objects.filter(username=username, phone_number=phone_number).first()

            if user:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('instructions')
            else:
                try:
                    user = User.objects.create_user(username=username, phone_number=phone_number)
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    return redirect('instructions')
                except Exception as e:
                    error = f"Error creating user: {str(e)}"
        else:
            error = "Both fields are required."

    return render(request, 'auth.html', {'error': error})


@login_required
def instructions(request):
    progress, _ = UserProgress.objects.get_or_create(user=request.user)

    if progress.seen_instructions:
        return redirect('home')

    if request.method == "POST":
        progress.seen_instructions = True
        progress.save()
        return redirect('home')

    return render(request, 'instructions.html')


@login_required
def home(request):
    progress, _ = UserProgress.objects.get_or_create(user=request.user)
    categories = Category.objects.all()
    return render(request, 'home.html', {'progress': progress, 'categories': categories})


@login_required
def start_test(request, category):
    progress, _ = UserProgress.objects.get_or_create(user=request.user)

    # Lock logic
    if category == "reading" and not progress.listening_passed:
        return redirect('home')
    if category == "writing" and not progress.reading_passed:
        return redirect('home')

    questions = list(Test.objects.filter(category=category))
    selected_questions = random.sample(questions, min(5, len(questions)))

    if request.method == "POST":
        score = 0
        for q in selected_questions:
            user_answer = request.POST.get(str(q.id))
            if user_answer == q.correct_answer:
                score += 1

        passed = score >= 3
        if category == "listening" and passed:
            progress.listening_passed = True
        if category == "reading" and passed:
            progress.reading_passed = True
        if category == "writing" and passed:
            progress.writing_passed = True
        progress.save()

        return render(request, 'result_popup.html', {'score': score, 'passed': passed})

    return render(request, 'test.html', {'questions': selected_questions, 'category': category})


def logout_view(request):
    logout(request)
    return redirect('auth')
