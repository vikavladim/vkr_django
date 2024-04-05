from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from schedule.views import menus
from teachers.forms import AddTeacherForm
from teachers.models import Teacher
from menus import *


def create(request):
    # return HttpResponse('creating teacher')
    # print('hello', sidebar_menu_base)
    # print('hellooooooooooooooooooooooooooooooooooooooooooo')
    context = {
        'title': 'creating teacher',
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu_base,
        'form': AddTeacherForm(),
    }
    return render(request, 'teachers/create.html', context)


def read(request, id):
    if id == 0:
        raise Http404
    elif id > 10:
        return redirect('home', permanent=True)
    # return HttpResponse(f'reading teacher {id}')
    context = {
        'title': f'reading teacher {id}',
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu_base,
        # 'posts': [val.values for val in Teacher.objects.all().values()],
        # 'fields': [f.name for f in Teacher._meta.fields],
    }
    return render(request, 'teachers/update.html', context)


def update(request, id):
    # return HttpResponse(f'updating teacher {id}')
    context = {
        'title': f'updating teacher {id}',
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu_base,
        # 'posts': [val.values for val in Teacher.objects.all().values()],
        # 'fields': [f.name for f in Teacher._meta.fields],
    }
    return render(request, 'teachers/update.html', context)


def delete(request, id):
    context = {
        'title': f'deleting teacher {id}',
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu_base,
    }
    return render(request, 'teachers/update.html', context)



def page_not_found(request, exception):
    print('exception', exception)
    return HttpResponseNotFound('Page not found', status=404)


def all(request):
    # new_teacher = Teacher.objects.create(
    #     fio="Петров Петр Петрович",
    #     photo="teachers/1.jpg",
    #     room=505,
    # )
    #
    # new_teacher.save()
    # temp=Menu(sidebar_menu)

    # for i in temp.items:
    #     print(i.text)
    print(request.path)
    context = {
        'title': 'Teachers',
        'teachers': [val for val in Teacher.objects.all()],
        'fields': [f.name for f in Teacher._meta.fields],
        'menu_selected': request.path,
    }
    # return render(request, 'teachers/teachers.html', context)
    return render(request, 'teachers/all.html', context)

