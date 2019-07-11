from django.contrib import admin
from lecturer.models import *
#from . import random_generator

class StudentsAllAdmin(admin.ModelAdmin):
    """Описание модели StudentsAll в админке"""
    fieldsets = [
        ('Имя студента:', {'fields': ['name']}),
        ('Группа:', {'fields': ['my_group']}),
        ('Активность:', {'fields': ['activity']})
    ]

    list_display = ('name_admin', 'my_group_admin', 'activity_admin')


class LectureAdmin(admin.ModelAdmin):
    """Описание модели Lecture в админке"""
    fieldsets = [
        ('Название лекции', {'fields': ['lecture_name']}),
        ('Дата', {'fields': ['time']}),
        ('Группы присутствующие на лекции', {'fields': ['group']})
    ]

    list_display = ('lecture_name_admin', 'time_admin', 'stud_count_admin')


admin.site.register(StudentsAll, StudentsAllAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Group)
#random_generator.run_random()