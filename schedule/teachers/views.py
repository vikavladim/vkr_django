from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from teachers.models import Teacher
from teachers.utils import DateMixin


class AddTeacher(DateMixin, CreateView):
    template_name = 'teachers/create.html'
    model = Teacher
    fields = ['fio', 'room', 'photo', 'subject']
    title = 'Создание учителя'
    success_url = reverse_lazy('teachers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, menu_selected=self.request.path, **kwargs)


# class DetailTeacher(DateMixin, DetailView):
#     model = Teacher
#     template_name = 'teachers/update.html'
#     context_object_name = 'teacher'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return self.get_mixin_context(context, title=context['teacher'].fio, menu_selected=self.request.path, **kwargs)


class UpdateTeacher(DateMixin, UpdateView):
    model = Teacher
    fields = ['fio', 'room', 'photo', 'subject']
    template_name = 'teachers/update.html'
    success_url = reverse_lazy('teachers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, teacher=context['teacher'], title=context['teacher'].fio,
                                      menu_selected=self.request.path, **kwargs)


def delete(request, id):
    context = {
        'title': f'deleting teacher {id}',
    }
    return render(request, 'teachers/update.html', context)


def page_not_found(request, exception):
    print('exception', exception)
    return HttpResponseNotFound('Page not found', status=404)


class TeacherListView(DateMixin, ListView):
    model = Teacher
    template_name = 'teachers/all.html'
    context_object_name = 'teachers'
    title = 'Учителя'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, menu_selected=self.request.path, **kwargs)


# def create_second_lists(request):
#     if request.method == 'POST':
#         form = TeacherFormSet(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/teachers')
#         else:
#             print(form.errors)
#     else:
#         form = TeacherFormSet()
#
#     context = {
#         'formset': form,
#         'menu_selected': request.path,
#     }
#     return render(request, 'teachers/create_list.html', context=context)

def getDataFromDB(request):
    selectedValue = request.GET.getlist('selectedValue[]')
    print(selectedValue)
    return HttpResponse(selectedValue)
