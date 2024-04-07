from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from schedule.views import menus
from teachers.forms import AddTeacherForm
from teachers.models import Teacher
from menus import *


# class AddTeacher(View):
#     def get(self, request):
#         form = AddTeacherForm()
#
#         context = {
#             'title': 'creating teacher',
#             'upper_menu': upper_menu,
#             'sidebar_menu': sidebar_menu_base,
#             'form': form,
#             'menu_selected': request.path,
#         }
#         return render(request, 'teachers/create.html', context)
#
#     def post(self, request):
#         form = AddTeacherForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')

# class AddTeacher(FormView):
#     template_name = 'teachers/create.html'
#     form_class = AddTeacherForm
#     success_url = reverse_lazy('teachers')
#     extra_context = {
#         'title': 'creating teacher',
#     }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu_selected'] = self.request.path
#         return context
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

class AddTeacher(CreateView):
    template_name = 'teachers/create.html'
    model = Teacher
    fields = ['fio', 'slug', 'room', 'photo', 'subject']
    extra_context = {
        'title': 'creating teacher',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_selected'] = self.request.path
        return context



class DetailTeacher(DetailView):
    model = Teacher
    template_name = 'teachers/update.html'
    context_object_name = 'teacher'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_selected'] = self.request.path
        context['title'] = context['teacher'].fio
        return context



# def update(request, id):
#     # return HttpResponse(f'updating teacher {id}')
#     context = {
#         'title': f'updating teacher {id}',
#         'upper_menu': upper_menu,
#         'sidebar_menu': sidebar_menu_base,
#         # 'posts': [val.values for val in Teacher.objects.all().values()],
#         # 'fields': [f.name for f in Teacher._meta.fields],
#     }
#     return render(request, 'teachers/update.html', context)

class UpdateTeacher(UpdateView):
    model = Teacher
    fields = ['fio', 'slug', 'room', 'photo', 'subject']
    template_name = 'teachers/create.html'
    success_url = reverse_lazy('teachers')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_selected'] = self.request.path
        context['title'] = context['teacher'].fio
        return context


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


class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/all.html'
    context_object_name = 'teachers'
    extra_context = {
        'title': 'Учителя',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_selected'] = self.request.path
        return context
