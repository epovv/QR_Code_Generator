from django import forms
from .models import *
from django.db.utils import OperationalError

try:
    class LectureForm(forms.Form):
        """Форма для записи лекции"""
        students_count = forms.IntegerField(
            min_value=0,
            max_value=len(StudentsAll.objects.all())
        )

        def save(self):
            new_lecture = Lecture.objects.create(
                students_count=self.cleaned_data['students_count']
            )
            return new_lecture
except OperationalError:
    pass  # Нельзя сделать makemigrations, т.к LectureForm ссылается на StudentsAll(Модель)


# class StudentsIsCameForm(forms.ModelForm):
#     """Форма для записи пришедшего студента по id к лекции"""
#     class Meta:
#         model = StudentsIsCame
#         fields = ['name', 'lecture']
