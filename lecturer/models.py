from django.db import models


class Group(models.Model):
    group_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return str(self.group_name)


class StudentsAll(models.Model):
    """БД содержащая всех студентов,
    для вывода списком по QR коду"""
    name = models.CharField(max_length=200)
    activity = models.BooleanField(default=True)
    my_group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

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
    )
    students_count = models.IntegerField()
    time = models.DateTimeField()
    student = models.ManyToManyField(StudentsAll, blank=True)
    group = models.ManyToManyField(Group, blank=True)

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'

    def __str__(self):
        return str(self.lecture_name)
