from django.contrib import admin
from .models import User, Filter, Category


class FilterInline(admin.TabularInline):
    model = Filter
    extra = 1  # Количество пустых полей для добавления новых фильтров


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Отображение имени и описания категории
    search_fields = ('name', 'description')  # Добавляем поиск по имени и описанию
    inlines = [FilterInline]  # Добавляем Inline для фильтров


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'address', 'phone')
    search_fields = ('first_name', 'last_name', 'city', 'address', 'phone')
    list_filter = ('city', 'address', 'phone')


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Отображение фильтра и категории
    list_filter = ('category',)  # Фильтрация по категории
    search_fields = ('name',)  # Поиск по имени