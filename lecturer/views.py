from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from datetime import datetime, date


@login_required(login_url='login')
def receiving_data(request):
    """Страница для ввода данных от лектора"""
    if request.method == 'GET':
        count = StudentsAll.objects.filter(activity=True).count()
        date_min = datetime.now().isoformat()[:-10]
        lecture_today = [
            i for i in Lecture.objects.all() if i.time.date() == date.today()
        ]
        return render(
            request,
            'lecturer/receiving_data.html',
            context={
                'count': count,
                'date_min': date_min,
                'lecture_today': lecture_today
            }
        )
    elif request.method == 'POST':
        id = Lecture.objects.create(
            lecture_name=request.POST['lecture_name'],
            students_count=request.POST['students_count'],
            time=datetime.strptime(request.POST['time'], '%Y-%m-%dT%H:%M')
        ).id
        return redirect('qr_generator_url', id)


def qr_generator(request, id):
    """Генератор QR кода"""
    if Lecture.objects.filter(id=id).exists():
        return render(
            request,
            'lecturer/QR.html',
            context={
                'link': request.build_absolute_uri('check_your_self/')
            }
        )
    else:
        raise Http404



def check(request, id):
    """Генерация ссылки для QR кода на шаблон
    для выбора студентов к конкретному id лекции с
    последующим созданием записи о присутсвующем студенте"""
    try:
        current_lect = Lecture.objects.get(id=id)
    except Lecture.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        if current_lect.time.date() == date.today():
            context = StudentsAll.objects.all()
            response = render(
                request,
                'lecturer/check_your_self.html',
                context={
                    'students': context,
                    'id': id,
                    'lecture': current_lect
                }
            )
            return response
        else:
            return HttpResponseForbidden(request)
    elif request.method == 'POST':
        if 'name' in request.COOKIES:
            messages.error(request, 'Вы уже отмечались сегодня!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if current_lect.student.count() < current_lect.students_count:
            current_lect.student.add(
                StudentsAll.objects.get(name=request.POST['Student'])
            )
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            messages.success(request, 'Вы отмечены! Спасибо за присутствие.')
            response.set_cookie('name', max_age=1)
            return response
        else:
            messages.error(request, 'Превышен лимит пришедших на лекцию!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
    """Регистрация"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, 'Ошибка')
            return redirect('registration_url')
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(
            request,
            'registration/registration.html',
            context=context
        )


def logout_view(request):
    """Выход из учетной запси"""
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'registration/logout.html')
    else:
        return redirect('login')


@login_required(login_url='login')
def lecture(request):
    """Статистика. Лекция - Студенты"""
    return render(request, 'lecturer/lecturer.html', {
            'lectures': Lecture.objects.all().order_by('-time')
        })


@login_required(login_url='login')
def student(request):
    """Статистика. Студент - Лекции"""
    return render(request, 'lecturer/students.html', {
            'students': StudentsAll.objects.all()
        })
