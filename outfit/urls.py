from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page_view, name='login_page_view'),
    path('register/', views.register_page_view, name='register_page_view'),
    path('logout/', views.logout_view, name='logout_view'),
]
