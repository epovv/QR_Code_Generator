from django.db import models
from django.shortcuts import reverse


class Group(models.Model):
    group_name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return str(self.group_name)


class StudentsAll(models.Model):
    """БД содержащая всех студентов,
    для вывода списком по QR коду"""
    name = models.CharField(max_length=200, unique=True)
    activity = models.BooleanField(default=True)
    my_group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['my_group']

    def __str__(self):
        return self.name

    def name_admin(self):
        return self.name
    name_admin.short_description = 'Студент'

    def my_group_admin(self):
        return self.my_group
    my_group_admin.short_description = 'Группа'

    def activity_admin(self):
        if self.activity:
            return 'Студент активен'
        else:
            return 'Студент не активен'
    activity_admin.short_description = 'Активность'


class Lecture(models.Model):
    """Для записи новых лекций лекторами
    по кол-ву пришедших студентов"""
    lecture_name = models.CharField(
        max_length=200,
    )
    students_count = models.IntegerField()
    time = models.DateTimeField()
    student = models.ManyToManyField(StudentsAll, blank=True)
    group = models.ManyToManyField(Group, blank=True)

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'
        ordering = ['-time']

    def __str__(self):
        return str(self.lecture_name)

    def lecture_name_admin(self):
        return self.lecture_name
    lecture_name_admin.short_description = 'Лекция'

    def time_admin(self):
        return self.time
    time_admin.short_description = 'Дата лекции'

    def stud_count_admin(self):
        return str(self.student.count()) + ' из ' + str(self.students_count)
    stud_count_admin.short_description = 'Студентов пришло'