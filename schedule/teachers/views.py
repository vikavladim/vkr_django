import json

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from cls.models import Class, TeacherDisciplineClass
from discipline.models import Discipline
from teachers.models import Teacher
from schedule.utils import DateMixin


class AddTeacher(DateMixin, CreateView):
    template_name = 'teachers/update.html'
    model = Teacher
    fields = ['fio', 'position', 'room', 'photo', 'discipline']
    title = 'Создание учителя'
    success_url = reverse_lazy('teachers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, menu_selected=self.request.path, **kwargs)


class UpdateTeacher(DateMixin, UpdateView):
    model = Teacher
    fields = ['fio', 'position', 'room', 'photo', 'discipline']
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
    teacher = get_object_or_404(Teacher, id=teacher_id) if teacher_id else None

    classes_by_disciplines = {'array': [], }

    for selectedValue in selected_values:
        discipline = get_object_or_404(Discipline, id=selectedValue)
        # classes_with_discipline = Class.objects.filter(discipline=discipline)
        classes_with_discipline = Class.objects.all()
                                   # .select_related('program'))
                                   # .filter(discipline=discipline)
        print(classes_with_discipline)
        selected_classes_strs = TeacherDisciplineClass.objects.filter(discipline=discipline, teacher=teacher)

        discipline_data = {
            'discipline': discipline.serializable,
            'classes': [cls.serializable for cls in classes_with_discipline],
            'selectedClassesId': [selected_str._class.id for selected_str in selected_classes_strs],
        }

        classes_by_disciplines['array'].append(discipline_data)

    return JsonResponse(classes_by_disciplines)


@csrf_exempt
def classes_field_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        disciplines_array = data.get('array')
        teacher_id = data.get('teacher_id')
        teacher = get_object_or_404(Teacher, id=teacher_id)
        old_objects = TeacherDisciplineClass.objects.filter(teacher=teacher)
        new_objects = []

        for discipline in disciplines_array:
            for class_id in discipline['classes']:
                new_objects.append(TeacherDisciplineClass(
                    teacher=teacher,
                    discipline=get_object_or_404(Discipline, id=discipline['id_discipline']),
                    _class=get_object_or_404(Class, id=class_id),
                ))

        deleted_objects = [obj.id for obj in old_objects if obj not in new_objects]
        added_objects = [obj for obj in new_objects if obj not in old_objects]

        all_objects = TeacherDisciplineClass.objects.all()

        for old_obj in all_objects:
            for add_abj in added_objects:
                if old_obj._class == add_abj._class and old_obj.discipline == add_abj.discipline:
                    deleted_objects.append(old_obj.id)

        TeacherDisciplineClass.objects.filter(id__in=deleted_objects).delete()
        TeacherDisciplineClass.objects.bulk_create(added_objects)

    return HttpResponse('ok')


class DeleteTeacher(DateMixin, DeleteView):
    model = Teacher
    template_name = 'teachers/delete.html'
    success_url = reverse_lazy('teachers')

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            menu_selected=self.request.path,
            **kwargs
        )
