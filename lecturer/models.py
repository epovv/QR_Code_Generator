from django.db import models
from django.utils import timezone

class StudentsAll(models.Model):
    """БД содержащая всех студентов,
    для вывода списком по QR коду"""
    name = models.CharField(max_length=200)
    activity = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Имя студента'
        verbose_name_plural = 'Имена студентов'

    def __str__(self):
        return self.name


class Lecture(models.Model):
    """Для записи новых лекций лекторами
    по кол-ву пришедших студентов"""
    lecture_name = models.CharField(
        max_length=200,
        default='Лекция'
    )
    students_count = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    student = models.ManyToManyField(StudentsAll, blank=True)

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'

    def __str__(self):
        return str(self.lecture_name)
