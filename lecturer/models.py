from django.db import models


class Course(models.Model):
    """БД для курсов"""
    course_name = models.CharField(
        verbose_name='Название курса',
        max_length=200,
        unique=True
    )
    activity = models.BooleanField(verbose_name='Активность', default=True)
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return str(self.course_name)


class Group(models.Model):
    """БД содержащая группы студентов"""
    group_name = models.CharField(
        verbose_name='Название группы',
        max_length=200,
        unique=True,
    )
    course = models.ForeignKey(
        Course,
        verbose_name='Курс',
        on_delete=models.CASCADE,
    )
    start_date = models.DateField(verbose_name='Дата начала обучения')
    end_date = models.DateField(verbose_name='Дата окончания обучения')
    activity = models.BooleanField(verbose_name='Активность', default=True)
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return str(self.group_name)

    def stud_count_admin(self):
        return str(StudentsAll.objects.filter(
            my_group__group_name=self.group_name
        ).count())
    stud_count_admin.short_description = 'Студентов в группе'


class StudentsAll(models.Model):
    """БД содержащая всех студентов, их активность и
    к какой группе принадлежат"""
    name = models.CharField(
        verbose_name='Студент',
        max_length=200,
        unique=True)
    start_date = models.DateField(verbose_name='Дата зачисления студента')
    activity = models.BooleanField(verbose_name='Активность', default=True)
    my_group = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        # ordering = ['my_group']

    def __str__(self):
        return self.name


class Lecture(models.Model):
    """Для записи новых лекций лекторами
    по кол-ву пришедших студентов"""
    lecture_name = models.CharField(
        verbose_name='Лекция',
        max_length=200,
    )
    students_count = models.IntegerField(default=0)
    time = models.DateTimeField(verbose_name='Дата лекции')
    student = models.ManyToManyField(
        StudentsAll,
        verbose_name='Студенты',
        blank=True
    )
    group = models.ManyToManyField(Group, verbose_name='Группа', blank=True)
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True
    )

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'
        ordering = ['-time']

    def __str__(self):
        return str(self.lecture_name)

    def stud_count_admin(self):
        return str(self.student.count()) + ' из ' + str(self.students_count)
    stud_count_admin.short_description = 'Студентов пришло'
