from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages


@login_required(login_url='login')
def receiving_data(request):
    """Страница для ввода данных от лектора"""
    if request.method == 'GET':
        count = len(StudentsAll.objects.all())
        return render(
            request,
            'lecturer/receiving_data.html',
            context={'count': count}
        )
    elif request.method == 'POST':
        Lecture.objects.create(
            students_count=request.POST['students_count']
        )
        id = Lecture.objects.last().id
        return redirect('qr_generator_url', id)


def qr_generator(request, id):
    """Генератор QR кода"""
    try:
        if Lecture.objects.get(id__iexact=id):
            response = render(
                request,
                'lecturer/QR.html',
                context={
                    'link': request.build_absolute_uri('check_your_self/')
                }
            )
    except Lecture.DoesNotExist:
        raise Http404
    return response


def check(request, id):
    """Генерация ссылки для QR кода на шаблон
    для выбора студентов к конкретному id лекции с
    последующим созданием записи о присутсвующем студенте"""
    lect = Lecture.objects.get(id=id)
    if request.method == 'GET':
        try:
            if lect:
                context = [
                    item.name for item in StudentsAll.objects.all()
                ]

                response = render(
                    request,
                    'lecturer/check_your_self.html',
                    context={
                        'name': context,
                        'id': id,
                        'lecture': Lecture.objects.get(id=id)
                    }
                )
        except Lecture.DoesNotExist:
            raise Http404
        return response
    elif request.method == 'POST':
        if 'name' in request.COOKIES:
            messages.error(request, 'Вы уже отмечались сегодня!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if Lecture.objects.get(id=id).student.count()\
                < Lecture.objects.get(id=id).students_count:
            stud = StudentsAll.objects.get(name=request.POST['Student'])
            Lecture.objects.get(id=id).student.add(StudentsAll.objects.get(id=stud.pk))
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            messages.success(request, 'Вы отмечены! Спасибо за присутствие.')
            return response
        else:
            messages.error(request, 'Превышен лимит пришедших на лекцию!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
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
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'registration/logout.html')
    else:
        return redirect('login')


@login_required(login_url='login')
def lecture(request):
    return render(request, 'lecturer/lecturer.html', {
            'lectures': Lecture.objects.all(),
        })


@login_required(login_url='login')
def student(request):
    return render(request, 'lecturer/students.html', {
            'students': StudentsAll.objects.all(),
        })
