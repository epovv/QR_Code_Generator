from django.contrib import admin
from lecturer.models import *
from django.contrib.auth import models


class StudentsAllAdmin(admin.ModelAdmin):
    """Описание модели StudentsAll в админке"""
    fieldsets = [
        ('Имя студента:', {'fields': ['name']}),
        ('Группа:', {'fields': ['my_group']}),
        ('Дата зачисления:', {'fields': ['start_date']}),
        ('Активность:', {'fields': ['activity']}),
        ('Комментарий:', {'fields': ['comment']}),
    ]

    list_display = ('name', 'activity', 'start_date')
    list_filter = ('my_group', 'activity', 'start_date')


class StudentsAllInLines(admin.TabularInline):
    """Для добавления новых студентов прямо в группах"""
    model = StudentsAll.my_group.through
    extra = 2


class LectureAdmin(admin.ModelAdmin):
    """Описание модели Lecture в админке"""
    fieldsets = [
        ('Название лекции:', {'fields': ['lecture_name']}),
        ('Дата:', {'fields': ['time']}),
        ('Группы присутствующие на лекции:', {'fields': ['group']}),
        ('Комментарий:', {'fields': ['comment']})
    ]

    list_display = ('lecture_name', 'time', 'stud_count_admin')
    list_filter = ('time', 'group')


class GroupAdmin(admin.ModelAdmin):
    """Описание модели Group в админке"""
    list_display = (
        'group_name',
        'course',
        'start_date',
        'end_date',
        'stud_count_admin',
        'activity'
    )
    list_filter = ('course', 'start_date', 'activity')
    inlines = (
        StudentsAllInLines,
    )


class GroupInLines(admin.StackedInline):
    """Для создания новых групп прямо в курсах"""
    model = Group
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    """Описание модели Course в админке"""
    list_display = ('course_name', 'activity')
    list_filter = ('activity', )

    inlines = (
        GroupInLines,
    )

admin.site.register(StudentsAll, StudentsAllAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Course, CourseAdmin)

admin.site.unregister(models.Group)
admin.site.unregister(models.User)
