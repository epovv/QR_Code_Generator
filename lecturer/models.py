from django.db import models


class StudentsAll(models.Model):
    """БД содержащая всех студентов,
    для вывода списком по QR коду"""
    name = models.CharField(max_length=200)


class Lecture(models.Model):
    """Для записи новых лекций лекторами
    по кол-ву пришедших студентов"""
    students_count = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class StudentsIsCame(models.Model):
    """Записи студентов, пришедших
    на конкретную лекцию."""
    name = models.CharField(max_length=200)
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
