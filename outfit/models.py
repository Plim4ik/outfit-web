from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='Группы',
        blank=True,
        related_name='customer_set'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='Права пользователя',
        blank=True,
        related_name='customer_permissions_set'
    )
    city = models.CharField(max_length=100, verbose_name='Город', blank=True, null=True)
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название вещи')
    filters = models.ManyToManyField('Category', related_name='foods', verbose_name='Категория')
    image = models.ImageField(upload_to='items/', verbose_name='Изображение вещи', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'
    
    def __str__(self):
        return self.name


class Outfit(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название образа')
    image = models.ImageField(upload_to='outfits/', verbose_name='Изображение образа', blank=True, null=True)
    items = models.ManyToManyField(Item, verbose_name='Вещи в образе', related_name='outfits')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Образ'
        verbose_name_plural = 'Образы'

    def __str__(self):
        return f"Образ {self.name}"