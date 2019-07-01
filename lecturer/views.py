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
        form = LectureForm()
        return render(
            request,
            'lecturer/receiving_data.html',
            context={'form': form}
        )
    elif request.method == 'POST':
        bound_form = LectureForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
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
    if request.method == 'GET':
        # Если лекция под таким id существует генерируется QR иначе 404
        try:
            if Lecture.objects.get(id__iexact=id):
                context = [
                    item.name for item in StudentsAll.objects.all()
                ]
                students_list = [
                    item['name'] for item in
                    StudentsIsCame.objects.values('name').filter(
                        lecture__id=id
                    )
                ]
                response = render(
                    request,
                    'lecturer/check_your_self.html',
                    context={
                        'name': context,
                        'id': id,
                        'students': students_list
                    }
                )
        except Lecture.DoesNotExist:
            raise Http404
        return response
    elif request.method == 'POST':
        if 'name' in request.COOKIES:
            messages.error(request, 'Вы уже отмечались сегодня!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # Ограничение создания записи по students_count от лектора
        if len(StudentsIsCame.objects.values('name').filter(lecture__id=id))\
                < Lecture.objects.get(id=id).students_count:
            new_student = StudentsIsCame(
                name=request.POST['Student'],
                lecture=Lecture.objects.get(id=id)
            )
            new_student.save()
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            response.set_cookie('name', max_age=5)  # max_age=86400 - сутки
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
    """Статистика. Лекция - Студенты"""
    count = [StudentsIsCame.objects.filter(lecture_id=i.id).count() for i in
             Lecture.objects.all()]
    students = StudentsIsCame.objects.all()
    lecture = list(zip(Lecture.objects.all(), count))
    return render(
        request,
        'lecturer/lecturer.html',
        context={'lec': lecture, 'stud': students}
    )


@login_required(login_url='login')
def student(request):
    """Статистика. Студент - Лекции"""
    stud = StudentsAll.objects.all()
    lect = [[j.lecture for j in
             StudentsIsCame.objects.filter(name=i.name).order_by('lecture_id')]
            for i in stud]
    new = list(zip(stud, lect))
    return render(request, 'lecturer/student.html', context={'new':new})
