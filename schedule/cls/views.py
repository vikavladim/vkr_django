import datetime
import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, CreateView, DeleteView

from discipline.models import Discipline
from program.models import ProgramDisciplines, Program
from .models import Class, TeacherDisciplineClass
from schedule.utils import DateMixin
from teachers.models import Teacher


class UpdateClass(DateMixin, UpdateView):
    model = Class
    template_name = 'classes/update.html'
    context_object_name = 'class'
    fields = ['program', 'digit', 'letter', ]
    success_url = reverse_lazy('classes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cls = context['class']

        return self.get_mixin_context(
            context,
            title=cls,
            menu_selected=self.request.path,
            select_disciplines_ids=ProgramDisciplines.objects.filter(program=cls.program).values_list('discipline_id', flat=True),
            all_disciplines=Discipline.objects.all(),
            id=cls.id,
            **kwargs
        )


class CreateClass(DateMixin, CreateView):
    model = Class
    template_name = 'classes/update.html'
    context_object_name = 'class'
    fields = ['program', 'digit', 'letter']
    success_url = reverse_lazy('classes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Создание класса',
            all_disciplines=Discipline.objects.all(),
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
    cls_id = request.GET.get('classId')
    program_id = request.GET.get('programId')

    if cls_id:
        cls = get_object_or_404(Class, id=cls_id)
    else:
        cls = None

    teachers_and_load_by_disciplines = {'array': [], }
    if program_id:
        program = get_object_or_404(Program, id=program_id)
    else:
        program = None

    for selectedValue in selected_values:
        discipline = get_object_or_404(Discipline, id=selectedValue)
        teachers = Teacher.objects.filter(discipline=discipline)
        selected_teacher_strs = TeacherDisciplineClass.objects.filter(discipline=discipline, cls=cls).first()
        load_str = ProgramDisciplines.objects.filter(program=program, discipline=discipline).first()
        load = load_str.load if load_str else 1

        discipline_data = {
            'discipline': discipline.serializable,
            'teachers': [t.serializable for t in teachers],
            'selectedTeacherId': selected_teacher_strs.teacher.id if selected_teacher_strs else None,
            'load': load
        }

        teachers_and_load_by_disciplines['array'].append(discipline_data)

    return JsonResponse(teachers_and_load_by_disciplines)


@csrf_exempt
def teachers_field_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        disciplines_array = data.get('array')
        class_id = data.get('class_id')
        program_id = data.get('program_id')
        class_digit = data.get('digit')
        letter = data.get('letter')

        if program_id:
            program = get_object_or_404(Program, id=program_id)
        else:
            program = Program.objects.create(digit=class_digit,
                                             name=f'Индивидуальная программа для {class_digit + letter} от {datetime.datetime.now()}')
            for discipline in disciplines_array:
                dis = get_object_or_404(Discipline, id=discipline['id_discipline'])
                ProgramDisciplines.objects.create(program=program, discipline=dis, load=discipline['load'])

        if class_id:
            cls = get_object_or_404(Class, id=class_id)
            cls.digit=class_digit
            cls.letter=letter
            cls.program=program
            cls.save()
        else:
            cls = Class.objects.create(digit=class_digit, letter=letter, program=program)

        old_objects = TeacherDisciplineClass.objects.filter(cls=cls)
        new_objects = []

        for discipline in disciplines_array:
            sub = get_object_or_404(Discipline, id=discipline['id_discipline'])

            if discipline['teacher']:
                new_objects.append(TeacherDisciplineClass(
                    teacher=get_object_or_404(Teacher, id=discipline['teacher']),
                    discipline=sub,
                    cls=cls,
                ))
            else:
                old_objects.filter(discipline=sub, cls=cls).delete()

        deleted_objects = [obj.id for obj in old_objects if obj not in new_objects]
        added_objects = [obj for obj in new_objects if obj not in old_objects]

        all_objects = TeacherDisciplineClass.objects.all()

        for old_obj in all_objects:
            for add_obj in added_objects:
                if old_obj.cls == add_obj.cls and old_obj.discipline == add_obj.discipline:
                    deleted_objects.append(old_obj.id)

        TeacherDisciplineClass.objects.filter(id__in=deleted_objects).delete()
        TeacherDisciplineClass.objects.bulk_create(added_objects)

    return HttpResponse('ok')


@csrf_exempt
def changeDisciplines(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        program_id = data.get('program_id')
        program = get_object_or_404(Program, id=program_id)

        return JsonResponse({
            'all_disciplines': [d.serializable for d in Discipline.objects.all()],
            'select_disciplines_ids': list(
                ProgramDisciplines.objects.filter(program=program).values_list('discipline_id', flat=True))
        })

    return HttpResponse('ne ok', status=400)
