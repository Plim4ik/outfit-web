from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Item
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Item, Outfit, Favorites
import logging

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'index.html')


def wardrobe_welcome(request):
    items = Item.objects.all()
    selected_items = request.session.get('selected_items', [])

    context = {
        'items': items,
        'selected_items': selected_items,
    }
    return render(request, 'item_picker.html', context)


def toggle_item(request, item_id):
    selected_items = request.session.get('selected_items', [])
    item_id_str = str(item_id)

    if item_id_str in selected_items:
        selected_items.remove(item_id_str)
        selected = False
    else:
        selected_items.append(item_id_str)
        selected = True

    request.session['selected_items'] = selected_items

    return JsonResponse({'selected': selected, 'item_id': item_id})


def recommendations(request):
    selected_item_ids = request.session.get('selected_items', [])
    selected_items = Item.objects.filter(id__in=selected_item_ids)

    outfits = Outfit.objects.filter(items__in=selected_items).distinct()

    # Получаем список избранных образов для текущего пользователя
    if request.user.is_authenticated:
        favorites = Favorites.objects.filter(user=request.user).first()
        favorite_outfits = favorites.outfits.all() if favorites else []
    else:
        favorite_outfits = []

    context = {
        'outfits': outfits,
        'selected_items': selected_items,
        'favorite_outfits': favorite_outfits,
    }
    return render(request, 'recommendations.html', context)


def toggle_favorite(request, outfit_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Вы не авторизованы. Войдите в аккаунт.'}, status=401)
    
    outfit = get_object_or_404(Outfit, id=outfit_id)
    
    # Получаем список избранного пользователя
    favorites, created = Favorites.objects.get_or_create(user=request.user)
    
    if outfit in favorites.outfits.all():
        # Удаляем образ из избранного
        favorites.outfits.remove(outfit)
        return JsonResponse({'success': 'Образ удален из избранного!', 'status': 'removed'}, status=200)
    else:
        # Добавляем образ в избранное
        favorites.outfits.add(outfit)
        return JsonResponse({'success': 'Образ добавлен в избранное!', 'status': 'added'}, status=200)

def favorite_outfits(request):
    if not request.user.is_authenticated:
        return redirect('login_page_view')
    # Get the logged-in user's favorites
    favorites = Favorites.objects.filter(user=request.user).first()
    if favorites:
        favorite_outfits = favorites.outfits.all()
    else:
        favorite_outfits = []

    context = {
        'favorite_outfits': favorite_outfits,
    }
    return render(request, 'favorite_outfits.html', context)


def login_page_view(request):
    if request.user.is_authenticated:
        return redirect('my_requests')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
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


        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password1
        )
        
        user.save()

        login(request, user)
        messages.success(request, "Вы успешно зарегистрировались!")
        return redirect('home')

    return render(request, 'auth/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login_page_view')