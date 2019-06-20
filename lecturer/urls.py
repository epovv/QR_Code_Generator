"""QRcode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from .views import *
from qr_code import urls as qr_code_urls

urlpatterns = [
    path('', receiving_data, name='receiving_data_url'),
    path('registration/', register, name='registration_url'),
    path('qr/<int:id>/', qr_generator, name='qr_generator_url'),
    path('qr/<int:id>/check_your_self/', check, name='check_your_self_url'),
    path('logout/', logout_view, name='logout'),
]
