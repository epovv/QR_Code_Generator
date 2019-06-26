from django.db import models


class StudentsAll(models.Model):
    """БД содержащая всех студентов,
    для вывода списком по QR коду"""
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Имя студента'
        verbose_name_plural = 'Имена студентов'

    def __str__(self):
        return self.name


class Lecture(models.Model):
    """Для записи новых лекций лекторами
    по кол-ву пришедших студентов"""
    students_count = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'

    def __str__(self):
        return ' Лекция № ' + str(self.id)


class StudentsIsCame(models.Model):
    """Записи студентов, пришедших
    на конкретную лекцию."""
    name = models.CharField(max_length=200)
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Пришедший студент'
        verbose_name_plural = 'Пришедшие студенты'
