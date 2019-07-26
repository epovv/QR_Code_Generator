from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q


@login_required(login_url='login')
def main_page(request):
    """Главная страница с сегодняшними лекциями"""
    lecture_today = Lecture.objects.filter(time__date=timezone.now())
    paginator = Paginator(lecture_today, 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginator = page.has_other_pages()
    return render(
        request,
        'lecturer/main_page.html',
        context={'lecture_today': page, 'is_paginated': is_paginator}
    )


@login_required(login_url='login')
def receiving_data(request):
    """Страница для ввода данных от лектора"""
    if request.method == 'GET':
        groups = Group.objects.filter(activity=True, course__activity=True)
        date_min = datetime.now().isoformat()[:-10]
        return render(
            request,
            'lecturer/receiving_data.html',
            context={'groups': groups, 'date_min': date_min}
        )
    elif request.method == 'POST':
        post_groups = request.POST.getlist('groups')
        query_groups = Group.objects.filter(group_name__in=post_groups)
        students_came = StudentsAll.objects.filter(
            activity=True,
            my_group__group_name__in=post_groups
        ).count()
        created_object = Lecture.objects.create(
            lecture_name=request.POST['lecture_name'],
            students_count=students_came,
            time=datetime.strptime(request.POST['time'], '%Y-%m-%dT%H:%M'),
            comment=request.POST['comment']
        )
        created_object.group.add(*query_groups)
        id = created_object.id
        return redirect('qr_generator_url', id)


def qr_generator(request, id):
    """Генератор QR кода"""
    if Lecture.objects.filter(id=id).exists():
        return render(
            request,
            'lecturer/QR.html',
            context={
                'link': request.build_absolute_uri('check/'),
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
        if current_lect.time.date() == timezone.now().date():
            search_query = request.GET.get('group', '')
            if search_query:
                students = StudentsAll.objects.filter(
                    my_group__group_name=search_query
                )
                groups = None
            else:
                groups = current_lect.group.all()
                students = None
            response = render(
                request,
                'lecturer/check_your_self.html',
                context={
                    'students': students,
                    'groups': groups,
                    'lecture': current_lect
                }
            )
            return response
        else:
            return HttpResponseForbidden(request)
    elif request.method == 'POST':
        print(request.POST['Student'])
        if 'name' in request.COOKIES:
            messages.error(request, 'Вы уже отмечались сегодня!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        current_lect.student.add(
            StudentsAll.objects.get(name=request.POST['Student'])
        )
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.success(request, 'Вы отмечены! Спасибо за присутствие.')
        response.set_cookie('name', max_age=0)
        return response


def logout_view(request):
    """Выход из учетной запси"""
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def lecture(request):
    """Статистика. Лекции"""
    group_filter = Group.objects.filter(
        Q(course__activity=True) & Q(activity=True)
    )
    search_query = request.GET.get('group', '')
    if search_query:
        lectures = Lecture.objects.filter(group__group_name=search_query)
    else:
        lectures = Lecture.objects.all()
    paginator = Paginator(lectures, 4)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginator = page.has_other_pages()
    return render(
        request,
        'lecturer/lectures.html',
        context={
            'lectures': page,
            'is_paginated': is_paginator,
            'groups': group_filter,
            'search_query': search_query
        }
    )


@login_required(login_url='login')
def lecture_more(request, id):
    """Статистика. Подробнее о лекции"""
    current_lect = Lecture.objects.get(id=id)
    if request.method == 'GET':
        search_query = request.GET.get('group', '')
        if search_query:
            students = StudentsAll.objects.filter(
                my_group__group_name=search_query
            )
            groups = None
        else:
            groups = current_lect.group.all()
            students = None
        response = render(
            request,
            'lecturer/lecture_more.html',
            context={
                'students': students,
                'groups': groups,
                'lecture': current_lect
            }
        )
        return response
    if request.method == 'POST':
        current_lect.student.remove(
            StudentsAll.objects.get(name=request.POST['Student'])
        )
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return response


@login_required(login_url='login')
def student(request):
    """Статистика. Студент - Лекции"""
    search_query = request.GET.get('search', '')
    if search_query:
        search_paginator = True
        students = StudentsAll.objects.filter(
            Q(my_group__activity=True) &
            Q(my_group__course__activity=True) & (
            Q(id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(my_group__group_name__icontains=search_query)
            )
        ).order_by('id').distinct()
    else:
        search_paginator = False
        students = StudentsAll.objects.filter(
            Q(my_group__activity=True) &
            Q(my_group__course__activity=True)
        )
    paginator = Paginator(students, 6)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginator = page.has_other_pages()
    return render(
        request,
        'lecturer/students.html',
        context={
            'students': page,
            'is_paginated': is_paginator,
            'search_paginator': search_paginator,
            'search_query': search_query
        }
    )


@login_required(login_url='login')
def student_more(request, id):
    student = StudentsAll.objects.get(id=id)
    courses = set([group.course for group in student.my_group.all()])
    return render(
        request, 'lecturer/student_more.html', context={
            'student': student,
            'courses': courses
        }
    )
