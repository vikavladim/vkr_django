from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from menus import *

menus = [
    {'url': '/home', 'title': 'Главная'},
    {'url': '/teachers', 'title': 'Учителя'},
    {'url': '/classes', 'title': 'Классы'},
    {'url': '/subjects', 'title': 'Предметы'},
    {'url': '/schedule', 'title': 'Расписание'},
]

# def home(request):
#     context = {
#         # 'upper_menu': upper_menu,
#         # 'sidebar_menu': sidebar_menu_base,
#         'menu_selected': menus[0]['url'],
#     }
#     return render(request, 'main_base.html', context)

class HomeView(TemplateView):
    template_name = 'main_base.html'
    extra_context = {
        'menu_selected': menus[0]['url'],
    }

def classes(request):
    print(request.path)
    context = {
        # 'upper_menu': upper_menu,
        # 'sidebar_menu': sidebar_menu_base,
        'menu_selected': request.path,
    }
    return render(request, 'classes.html', context)

def subjects(request):
    print(request.path)
    context = {
        'menu_selected': request.path,
    }
    return render(request, 'main_base.html', context)

def schedule(request):
    print(request.path)
    context = {
        'menu_selected': request.path,
    }
    return render(request, 'main_base.html', context)
