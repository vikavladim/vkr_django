import json

from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from teachers.forms import TeacherForm
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

        classes_by_subjects = {}
        subjects = context['teacher'].subject.all()

        for subject in subjects:
            classes = Class.objects.filter(subject=subject)
            classes_by_subjects[subject] = list(classes)

        # print(classes_by_subjects)

        return self.get_mixin_context(context,
                                      teacher=context['teacher'],
                                      title=context['teacher'].fio,
                                      id=context['teacher'].id,
                                      classes_by_subjects=classes_by_subjects,
                                      menu_selected=self.request.path, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        # form_values = {field: getattr(form.instance, field) for field in form.fields}
        #
        # print(form_values)
        # print(form)

        return response


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
    selectedValues = request.GET.getlist('selectedValues[]')

    classes_by_subjects = {'array': [], }

    for selectedValue in selectedValues:
        subject = get_object_or_404(Discipline, id=selectedValue)
        classes_with_subject = Class.objects.filter(subject=subject)

        subject_data = {
            'subject': subject.serializable,
            'classes': [cls.serializable for cls in classes_with_subject]
        }

        classes_by_subjects['array'].append(subject_data)

    return JsonResponse(classes_by_subjects)


def test_for_forms(request, slug):
    # print('hello')
    if request.method == 'POST':
        greetings = request.POST.getlist('form')
        data = greetings.POST.getlist('id_select-3_to')
        print(greetings)
        return render(request, 'teachers/all.html', )
    else:
        teacher = get_object_or_404(Teacher, slug=slug)
        form = TeacherForm(instance=teacher)
        return render(request, 'teachers/update.html', context={'form': form})


@csrf_exempt
def my_test_process(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        array = data.get('array')
        teacher_id = data.get('teacher_id')
        # print(teacher)
        # print(array)
        for subject in array:
            for class_id in subject['classes']:
                TeacherSubjectClass.objects.create(
                    teacher=get_object_or_404(Teacher, id=teacher_id),
                    subject=get_object_or_404(Discipline, id=subject['id_subject']),
                    _class=get_object_or_404(Class, id=class_id),
                )

    return HttpResponse('ok')
