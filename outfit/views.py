from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Item
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Item, Outfit, Favorites

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
        selected = False  # Item is now unselected
    else:
        selected_items.append(item_id_str)
        selected = True   # Item is now selected

    request.session['selected_items'] = selected_items

    # Return a JSON response with the 'selected' status
    return JsonResponse({'selected': selected, 'item_id': item_id})




def recommendations(request):
    # Retrieve selected items from the session
    selected_item_ids = request.session.get('selected_items', [])
    selected_items = Item.objects.filter(id__in=selected_item_ids)

    # Get outfits that contain selected items
    outfits = Outfit.objects.filter(items__in=selected_items).distinct()

    context = {
        'outfits': outfits,
        'selected_items': selected_items,
    }
    return render(request, 'recommendations.html', context)


@login_required
def add_to_favorites(request, outfit_id):
    outfit = get_object_or_404(Outfit, id=outfit_id)

    # Check if the outfit is already in the user's favorites
    if Favorites.objects.filter(user=request.user, outfit=outfit).exists():
        messages.info(request, "Этот образ уже в вашем избранном!")
    else:
        # Add the outfit to favorites
        Favorites.objects.create(user=request.user, outfit=outfit)
        messages.success(request, "Образ добавлен в избранное!")

    return redirect('login_page_view')
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