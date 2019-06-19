from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *


def receiving_data(request):
    """Страница для ввода данных от лектора"""
    if request.method == 'GET':
        form = LectureForm()
        return render(request, 'lecturer/receiving_data.html', context={'form': form})
    elif request.method == 'POST':
        bound_form = LectureForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            id = Lecture.objects.last().id
            return redirect('qr/' + str(id))  # Редирект после добавления записи на QR по id


def qr_generator(request, id):
    """Генератор QR кода"""
    try:
        if Lecture.objects.get(id__iexact=id):
            response = render(
                request,
                'lecturer/QR.html',
                context={
                    'link': 'http://127.0.0.1:8000/qr/' + str(id) + '/check_your_self/'
                }
            )
    except Lecture.DoesNotExist:
        raise Http404
    return response


def check(request, id):
    """Генерация ссылки для QR кода на шаблон
    для выбора студентов к конкретному id лекции с
    последующим созданием записи о присутсвующем студенте"""
    if request.method == 'GET':
        # Если лекция под таким id существует генерируется QR иначе 404
        try:
            if Lecture.objects.get(id__iexact=id):
                context = StudentsAll.objects.all()
                response = render(request, 'lecturer/check_your_self.html', context={'name': context, 'id': id})
        except Lecture.DoesNotExist:
            raise Http404
        return response
    elif request.method == 'POST':
        # Ограничение создания записи по students_count от лектора
        if len(StudentsIsCame.objects.values(
                'name').filter(lecture__id=id)) < Lecture.objects.get(id=id).students_count:
            # Ограничение создания записи если этот студент уже отметился
            if request.POST['Student'] in \
                    [item['name'] for item in StudentsIsCame.objects.values('name').filter(lecture__id=id)]:
                return HttpResponse('Вы уже отметились!')
            else:
                new_student = StudentsIsCame(name=request.POST['Student'], lecture=Lecture.objects.get(id=id))
                new_student.save()
                return HttpResponse('Успех!')
        else:
            return HttpResponse('Привышен лимит пришедших на лекцию!')


def register(request):
    """Регистрация"""
    return render(request, 'registration/registration.html')
