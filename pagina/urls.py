"""
URL configuration for proyecto1programacion2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from .views import home
from .views import registro
from .views import profile
from . import views
from .views import upload_file, file_repository, edit_file,archivo


urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('registro/', registro, name='registro'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('archivo/', archivo, name='archivo'),
    path('upload_file/', upload_file, name='upload_file'),
    path('file_repository/', file_repository, name='file_repository'),
    path('edit_file/<int:file_id>', edit_file, name='edit_file'),




]
