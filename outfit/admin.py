from django.contrib import admin
from .models import User, Category, Item, Outfit


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    autocomplete_fields = ('items',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')
    autocomplete_fields = ('filters',)

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'address', 'phone')
    search_fields = ('first_name', 'last_name', 'city', 'address', 'phone')
    list_filter = ('city', 'address', 'phone')
