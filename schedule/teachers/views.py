import json

from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from teachers.models import Teacher, Class, Discipline, TeacherSubjectClass
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

        return self.get_mixin_context(context,
                                      teacher=context['teacher'],
                                      title=context['teacher'].fio,
                                      id=context['teacher'].id,
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


def getDataFromDB(request):
    selected_values = request.GET.getlist('selectedValues[]')
    teacher_id = request.GET.get('teacherId')
    teacher = get_object_or_404(Teacher, id=teacher_id)

    classes_by_subjects = {'array': [], }

    for selectedValue in selected_values:
        subject = get_object_or_404(Discipline, id=selectedValue)
        classes_with_subject = Class.objects.filter(subject=subject)
        selected_classes_strs = TeacherSubjectClass.objects.filter(subject=subject, teacher=teacher)

        subject_data = {
            'subject': subject.serializable,
            'classes': [cls.serializable for cls in classes_with_subject],
            'selectedClassesId': [selected_str._class.id for selected_str in selected_classes_strs],
        }

        classes_by_subjects['array'].append(subject_data)

    return JsonResponse(classes_by_subjects)


@csrf_exempt
def classes_field_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subjects_array = data.get('array')
        teacher_id = data.get('teacher_id')
        teacher = get_object_or_404(Teacher, id=teacher_id)
        old_objects = TeacherSubjectClass.objects.filter(teacher=teacher)
        new_objects = []

        for subject in subjects_array:
            for class_id in subject['classes']:
                new_objects.append(TeacherSubjectClass(
                    teacher=teacher,
                    subject=get_object_or_404(Discipline, id=subject['id_subject']),
                    _class=get_object_or_404(Class, id=class_id),
                ))

        deleted_objects = [obj.id for obj in old_objects if obj not in new_objects]
        added_objects = [obj for obj in new_objects if obj not in old_objects]

        all_objects = TeacherSubjectClass.objects.all()

        for old_obj in all_objects:
            for add_abj in added_objects:
                if old_obj._class == add_abj._class and old_obj.subject == add_abj.subject:
                    deleted_objects.append(old_obj.id)

        TeacherSubjectClass.objects.filter(id__in=deleted_objects).delete()
        TeacherSubjectClass.objects.bulk_create(added_objects)

    return HttpResponse('ok')
