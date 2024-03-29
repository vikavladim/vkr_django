from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from menus import *


def home(request):
    context = {
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu_base,
    }
    # return render(request, 'main_base.html')
    return render(request, 'main_base.html', context)

def classes(request):
    context = {
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu_base,
    }
    return render(request, 'classes.html', context)
