from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView

from discipline.models import Discipline
from models import Class
from schedule.utils import DateMixin
from teachers.models import Teacher


class UpdateClass(DateMixin, UpdateView):
    model = Class
    template_name = 'classes/update.html'
    context_object_name = 'class'
    fields = ['digit', 'letter', 'subject']
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
    fields = ['digit', 'letter', 'subject']
    success_url = reverse_lazy('classes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Создание класса',
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

    teachers_by_subjects = {'array': [], }

    for selectedValue in selected_values:
        subject = get_object_or_404(Discipline, id=selectedValue)
        teachers = Teacher.objects.filter(subject=subject)
        selected_teacher_strs = TeacherSubjectClass.objects.filter(subject=subject, _class=obj).first()
        load = Program.objects.filter(cls=obj, discipline=subject).first()

        subject_data = {
            'subject': subject.serializable,
            'teachers': [t.serializable for t in teachers],
            'selectedTeacherId': selected_teacher_strs.teacher.id if selected_teacher_strs else None,
            'load': load.load if load else None
        }

        teachers_by_subjects['array'].append(subject_data)

    return JsonResponse(teachers_by_subjects)


@csrf_exempt
def teachers_field_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subjects_array = data.get('array')
        class_id = data.get('class_id')
        cls = get_object_or_404(Class, id=class_id)
        old_objects = TeacherSubjectClass.objects.filter(_class=cls)
        new_objects = []

        for subject in subjects_array:
            sub = get_object_or_404(Discipline, id=subject['id_subject'])

            program_obj, created = Program.objects.get_or_create(cls=cls, discipline=sub)
            program_obj.load = subject['hours_week']
            program_obj.save()

            if subject['teacher']:
                new_objects.append(TeacherSubjectClass(
                    teacher=get_object_or_404(Teacher, id=subject['teacher']),
                    subject=sub,
                    _class=cls,
                ))
            else:
                old_objects.filter(subject=sub, _class=cls).delete()

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
