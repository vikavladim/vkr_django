import io

from django.forms import forms, widgets
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView
from pytils.translit import slugify
from xlsxwriter import Workbook

from schedule.forms import AddClassForm, ClassFormSet, SubjectFormSet
from teachers.models import Teacher, Class, Discipline, TeacherSubjectClass

import pandas as pd

from teachers.utils import DateMixin

menus = [
    {'url': '/home', 'title': 'Главная'},
    {'url': '/teachers', 'title': 'Учителя'},
    {'url': '/classes', 'title': 'Классы'},
    {'url': '/subjects', 'title': 'Предметы'},
    {'url': '/schedule', 'title': 'Расписание'},
    {'url': '/admin', 'title': 'Админка'},
]


class HomeView(TemplateView):
    template_name = 'main_base.html'
    extra_context = {
        'menu_selected': menus[0]['url'],
    }


def classes(request):
    print(request.path)
    context = {
        'menu_selected': request.path,
    }
    return render(request, 'classes.html', context)


def subjects(request):
    print(request.path)
    context = {
        'menu_selected': request.path,
    }
    return render(request, 'main_base.html', context)


def schedule(request):
    print(request.path)
    context = {
        'menu_selected': request.path,
    }
    return render(request, 'main_base.html', context)


def export_to_excel(request):
    elements = Teacher.objects.all()

    # df = pd.DataFrame(data)
    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    # r = Row and c = Column
    r = 0
    c = 0

    table_headers = [
        'ФИО',
        'URL',
        'Фото',
        'Кабинет',
        'Предметы'
    ]
    for header in table_headers:
        worksheet.write(r, c, header)
        c += 1

    r += 1
    for element in elements:
        worksheet.write(r, 0, element.fio)
        worksheet.write(r, 1, element.slug)
        # worksheet.write(r, 2, element.photo)
        worksheet.write(r, 3, element.room)
        r += 1

    workbook.close()
    output.seek(0)
    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = HttpResponse(output.read(), content_type=content_type)
    file_name = 'my_table'
    response['Content-Disposition'] = "attachment; filename=" + file_name + ".xlsx"
    return response


def create_class(request):
    if request.method == 'POST':
        form = ClassFormSet(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/classes')
        else:
            print(form.errors)
    else:
        form = ClassFormSet()

    context = {
        'formset': form,
        'menu_selected': request.path,
    }
    return render(request, 'classes/create_class.html', context=context)


class UpdateClass(DateMixin, UpdateView):
    model = Class
    template_name = 'classes/update.html'
    context_object_name = 'class'
    fields = ['digit', 'letter', 'subject']
    success_url = reverse_lazy('classes')

    # form_class = UpdateClassForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=context['class'],
            menu_selected=self.request.path,
            id=context['class'].id,
            **kwargs
        )


def create_subject(request):
    for o in Discipline.objects.all():
        o.slug = slugify(o.name)
        o.save()

    if request.method == 'POST':
        form = SubjectFormSet(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/subjects')
        else:
            print(form.errors)
    else:
        form = SubjectFormSet()

    context = {
        'formset': form,
        'menu_selected': request.path,
    }
    return render(request, 'subjects/all.html', context=context)


def getTeachersFromDB(request):
    selected_values = request.GET.getlist('selectedValues[]')
    obj_id = request.GET.get('classId')
    obj = get_object_or_404(Class, id=obj_id)

    teachers_by_subjects = {'array': [], }

    for selectedValue in selected_values:
        subject = get_object_or_404(Discipline, id=selectedValue)
        teachers = Teacher.objects.filter(subject=subject)
        selected_teacher_strs = TeacherSubjectClass.objects.filter(subject=subject, _class=obj).first()

        subject_data = {
            'subject': subject.serializable,
            'teachers': [t.serializable for t in teachers],
            'selectedTeacherId': selected_teacher_strs.teacher.id if selected_teacher_strs else None,
        }

        teachers_by_subjects['array'].append(subject_data)

    return JsonResponse(teachers_by_subjects)
