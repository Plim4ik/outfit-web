from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'index.html')



def login_page_view(request):
    if request.user.is_authenticated:
        return redirect('my_requests')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Аутентификация пользователя через email
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('my_requests')
        else:
            messages.error(request, 'Неверная почта или пароль.')
    
    return render(request, 'auth/login.html')

def register_page_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
            return redirect('register_page_view')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже зарегистрирован.")
            return redirect('register_page_view')

        # Создаем нового пользователя
        user = User.objects.create_user(
            username=email,  # Используем email как имя пользователя
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password1
        )
        
        user.save()

        login(request, user)  # Автоматически авторизуем пользователя после регистрации
        messages.success(request, "Вы успешно зарегистрировались!")
        return redirect('home')

    return render(request, 'auth/register.html')

# Выход из системы
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login_page_view')