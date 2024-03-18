from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect


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
    return render(request, 'teachers/teachers.html')
