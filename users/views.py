from django.http import HttpResponseBadRequest
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy

from pdf.forms import PdfForm
from .forms import *
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from pdf.models import Pdf

def login(request):
    """Функция для авторизации пользователя"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:profile_pdf'))

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home'))
        else:
            messages.warning(request, "Неправильный логин или пароль")
    else:
        form = UserLoginForm()
    context = {
        'form': form,
        'title': 'Авторизация',
    }
    return render(request,'users/login.html', context)

def register(request):
    """Функция для регистрации пользователя"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:profile_pdf'))
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            if User.objects.filter(username = request.POST['username']).first():
                messages.error(request, "Такой пользователь уже существует")
                return redirect('users:register')
            elif User.objects.filter(email = request.POST['email']).first():
                messages.error(request, "Пользователь с такой почтой уже существует")
                return redirect('users:register')
            else:
                form.save()
                messages.success(request, 'Вы успешно зарегистрировались')
                return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
        'title': 'Создание профиля',
    }
    return render(request, 'users/register.html', context)

def logout_user(request):
    """Функция логаута"""
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    """Функция для отображения профиля пользователя"""
    files = Pdf.objects.filter(user=request.user)
    count = len(files)
    form = UserProfileForm({"username": request.user.username,
                            'email': request.user.email})
    context = {
        'title': f"Профиль {request.user.username}",
        'count' : count,
        'form' : form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_pdf(request):
    """Функция для отображения файлов PDF/JPG в личном кабинете"""
    files = Pdf.objects.filter(user=request.user).order_by('-time_created')
    count = len(files)
    context = {
        'title': f"PDF/JPG {request.user.username}",
        'files' : files,
        'count' : count,
        'name' : 'PDF/JPG',
    }
    return render(request, 'users/profile_pdf.html', context)

