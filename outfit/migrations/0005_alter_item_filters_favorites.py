# Generated by Django 5.1.4 on 2024-12-21 07:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outfit', '0004_outfit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='filters',
            field=models.ManyToManyField(blank=True, related_name='foods', to='outfit.category', verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('outfit', models.ManyToManyField(related_name='favorites', to='outfit.outfit', verbose_name='Избранные образы')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
            },
        ),
    ]
