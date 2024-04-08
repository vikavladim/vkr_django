from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from teachers.models import Teacher
from menus import *
from teachers.utils import DateMixin


class AddTeacher(DateMixin, CreateView):
    template_name = 'teachers/create.html'
    model = Teacher
    fields = ['fio', 'slug', 'room', 'photo', 'subject']
    # extra_context = {
    #     'title': 'Создание учителя',
    # }
    title = 'Создание учителя'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, menu_selected=self.request.path, **kwargs)
        # context['menu_selected'] = self.request.path
        # return context


class DetailTeacher(DateMixin, DetailView):
    model = Teacher
    template_name = 'teachers/update.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['teacher'].fio, menu_selected=self.request.path, **kwargs)
        # context['menu_selected'] = self.request.path
        # context['title'] = context['teacher'].fio
        # return context


class UpdateTeacher(DateMixin, UpdateView):
    model = Teacher
    fields = ['fio', 'slug', 'room', 'photo', 'subject']
    template_name = 'teachers/create.html'
    success_url = reverse_lazy('teachers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['teacher'].fio, menu_selected=self.request.path, **kwargs)
        # context['menu_selected'] = self.request.path
        # context['title'] = context['teacher'].fio
        # return context


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


class TeacherListView(DateMixin, ListView):
    model = Teacher
    template_name = 'teachers/all.html'
    context_object_name = 'teachers'
    # extra_context = {
    #     'title': 'Учителя',
    # }
    title = 'Учителя'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, menu_selected=self.request.path, **kwargs)
        # context['menu_selected'] = self.request.path
        # return context
