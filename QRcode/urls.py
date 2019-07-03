from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lecturer.urls')),
    path('', include('django.contrib.auth.urls'), name='login_url'),
]
