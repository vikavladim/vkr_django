from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from teachers.models import Teacher

upper_menu = [
    {"text": "Home", "url": "#"},
    {"text": "Features", "url": "#"},
    {"text": "Pricing", "url": "#"},
    {"text": "FAQs", "url": "#"},
    {"text": "About", "url": "#"}
]

sidebar_menu = [
    {"text": "Teachers", "url": "/teachers"},
    {"text": "Dashboard", "url": "#"},
    {"text": "Orders", "url": "#"},
    {"text": "Products", "url": "#"},
    {"text": "Customers", "url": "#"}
]


def create(request):
    return HttpResponse('creating teacher')


def read(request, id):
    if id == 0:
        raise Http404
    elif id > 10:
        return redirect('home', permanent=True)
    return HttpResponse(f'reading teacher {id}')


def update(request, id):
    return HttpResponse(f'updating teacher {id}')


def delete(request, id):
    return HttpResponse(f'deleting teacher {id}')


def page_not_found(request, exception):
    print('ggggggggggggg')
    return HttpResponseNotFound('Page not found', status=404)


def all(request):
    # new_teacher = Teacher.objects.create(
    #     fio="Петров Петр Петрович",
    #     photo="teachers/1.jpg",
    #     room=505,
    # )
    #
    # new_teacher.save()

    fields=[f.name for f in Teacher._meta.fields]
    posts = [val.values for val in Teacher.objects.all().values()]

    context = {
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu,
        'posts': posts,
        'fields': fields,
    }
    return render(request, 'teachers/teachers.html', context)
