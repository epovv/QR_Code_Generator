from django.urls import path
from .views import *


urlpatterns = [
    path('', main_page, name='main_page_url'),
    path('create_lecture/', receiving_data, name='receiving_data_url'),
    path('qr/<int:id>/', qr_generator, name='qr_generator_url'),
    path('qr/<int:id>/check/', check, name='check_your_self_url'),
    path('logout/', logout_view, name='logout'),
    path('lectures/', lecture, name='lecture'),
    path('students/', student, name='student'),
    path('lectures/<int:id>', lecture_more, name='lecture_more_url'),
    path('students/<int:id>', student_more, name='student_more_url'),
]
