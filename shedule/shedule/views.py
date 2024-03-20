from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from menus import *


def home(request):
    context = {
        'upper_menu': upper_menu,
        'sidebar_menu': sidebar_menu,
    }
    return render(request, '../../teachers/templates/teachers/base.html', context)
