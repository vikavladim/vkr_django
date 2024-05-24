import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, CreateView, DeleteView

from discipline.models import Discipline
from .models import Class, Level, TeacherDisciplineClass
from schedule.utils import DateMixin
from teachers.models import Teacher


class UpdateClass(DateMixin, UpdateView):
    model = Class
    template_name = 'classes/update.html'
    context_object_name = 'class'
    fields = ['digit', 'letter', 'discipline']
    success_url = reverse_lazy('classes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=context['class'],
            menu_selected=self.request.path,
            id=context['class'].id,
            **kwargs
        )


class CreateClass(DateMixin, CreateView):
    model = Class
    template_name = 'classes/update.html'
    context_object_name = 'class'
    fields = ['level', 'digit', 'letter']
    success_url = reverse_lazy('classes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Создание класса',
            disciplines=Discipline.objects.all(),
            menu_selected=self.request.path,
            **kwargs
        )


class DeleteClass(DateMixin, DeleteView):
    model = Class
    template_name = 'classes/delete.html'
    success_url = reverse_lazy('classes')

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


def class_list(request):
    classes = Class.objects.all()
    students = {}

    for cls in classes:
        if cls.digit not in students:
            students[cls.digit] = []
        students[cls.digit].append(cls)

    context = {
        'title': 'Классы',
        'students': students,
        'menu_selected': request.path,
    }

    return render(request, 'classes/class_list.html', context)


def getTeachersFromDB(request):
    selected_values = request.GET.getlist('selectedValues[]')
    obj_id = request.GET.get('classId')
    obj = get_object_or_404(Class, id=obj_id)

    teachers_by_disciplines = {'array': [], }

    for selectedValue in selected_values:
        discipline = get_object_or_404(Discipline, id=selectedValue)
        teachers = Teacher.objects.filter(discipline=discipline)
        selected_teacher_strs = TeacherDisciplineClass.objects.filter(discipline=discipline, _class=obj).first()
        load = Program.objects.filter(cls=obj, discipline=discipline).first()

        discipline_data = {
            'discipline': discipline.serializable,
            'teachers': [t.serializable for t in teachers],
            'selectedTeacherId': selected_teacher_strs.teacher.id if selected_teacher_strs else None,
            'load': load.load if load else None
        }

        teachers_by_disciplines['array'].append(discipline_data)

    return JsonResponse(teachers_by_disciplines)


@csrf_exempt
def teachers_field_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        disciplines_array = data.get('array')
        class_id = data.get('class_id')
        cls = get_object_or_404(Class, id=class_id)
        old_objects = TeacherDisciplineClass.objects.filter(_class=cls)
        new_objects = []

        for discipline in disciplines_array:
            sub = get_object_or_404(Discipline, id=discipline['id_discipline'])

            program_obj, created = Program.objects.get_or_create(cls=cls, discipline=sub)
            program_obj.load = discipline['hours_week']
            program_obj.save()

            if discipline['teacher']:
                new_objects.append(TeacherDisciplineClass(
                    teacher=get_object_or_404(Teacher, id=discipline['teacher']),
                    discipline=sub,
                    _class=cls,
                ))
            else:
                old_objects.filter(discipline=sub, _class=cls).delete()

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


class CreateLevel(DateMixin, CreateView):
    model = Level
    template_name = 'classes/create_level.html'
    context_object_name = 'grade'
    fields = ['name', 'discipline']
    success_url = reverse_lazy('classes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Создание параллели',
            menu_selected=self.request.path,
            **kwargs
        )
