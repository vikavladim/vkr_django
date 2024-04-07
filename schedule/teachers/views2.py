from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from schedule.views import menus
from teachers.forms import AddTeacherForm
from teachers.models import Teacher
from menus import *


# def handle_uploaded_file(f):
#     with open(f"media/images/{f.name}.txt", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def create(request):
    # context = {
    #     'title': 'creating teacher',
    #     'upper_menu': upper_menu,
    #     'sidebar_menu': sidebar_menu_base,
    #     'form': AddTeacherForm(),
    # }
    # return render(request, 'teachers/create.html', context)
    if request.method == 'POST':
        form = AddTeacherForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['photo'])
            form.save()
            return redirect('home')
    else:
        form = AddTeacherForm()
    context = {
        'title': 'creating teacher',
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu_base,
        'form': form,
        'menu_selected': request.path,
    }
    return render(request, 'teachers/create.html', context)


# def read(request, id):
#     if id == 0:
#         raise Http404
#     elif id > 10:
#         return redirect('home', permanent=True)
#     # return HttpResponse(f'reading teacher {id}')
#     context = {
#         'title': f'reading teacher {id}',
#         'upper_menu': upper_menu,
#         'sidebar_menu': sidebar_menu_base,
#         # 'posts': [val.values for val in Teacher.objects.all().values()],
#         # 'fields': [f.name for f in Teacher._meta.fields],
#     }
#     return render(request, 'teachers/update.html', context)

def read(request, teacher_slug):
    teacher_name = get_object_or_404(Teacher, slug=teacher_slug).fio
    # teacher_name=Teacher.objects.get(slug=slug).name
    context = {
        'title': f'reading teacher {teacher_name}',
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu_base,
        'menu_selected': request.path,
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
