"""
URL configuration for My_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signout',views.signout, name='signout'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('settings/',views.settings, name='settings'),
    path('profile/',views.profile_view, name='profile'),
    path('helpcenter',views.helpcenter, name='helpcenter'),
    path('subscription/',views.subscription, name='subscription'),
    path('about_us/', views.about_us, name='about_us'),
    path('voice',views.process_voice,name='process_voice'),
    path('search/', views.search, name='search'),
    path('contact/',views.contact,name='contact'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('voice_search/', views.voice_search, name='voice_search'),
    path('genres/', views.genres_page, name='genres'),
    path('genres/<str:genre_name>/', views.genre_songs, name='genre_songs'),


]
