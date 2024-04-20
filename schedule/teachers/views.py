from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from teachers.models import Teacher, Class, Discipline
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

        classes_by_subjects = {}
        subjects = context['teacher'].subject.all()

        for subject in subjects:
            classes = Class.objects.filter(subject=subject)
            classes_by_subjects[subject] = list(classes)

        # print(classes_by_subjects)

        return self.get_mixin_context(context, teacher=context['teacher'], title=context['teacher'].fio,
                                      classes_by_subjects=classes_by_subjects,
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
    print("Мы зашли в getDataFromDB")
    selectedValue = request.GET.getlist('selectedValue')
    # selectedValue = request.GET.getlist('selectedValue[]')
    print(selectedValue)
    classes_by_subjects = {
        'array': [],
    }
    subject = get_object_or_404(Discipline, id=selectedValue[0])
    classes_with_subject = Class.objects.filter(subject=subject)
    # print(classes_with_subject)
    subject_data = {
        'subject': subject.serializable,
        'classes': [cls.serializable for cls in classes_with_subject]
    }

    classes_by_subjects['array'].append(subject_data)
    # print(classes_by_subjects)
    # for subject in subjects:
    #     classes = Class.objects.filter(subject=subject)
    #     classes_by_subjects[subject] = list(classes)
    return JsonResponse(classes_by_subjects)
