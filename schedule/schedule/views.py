import io
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView
from xlsxwriter import Workbook

from teachers.models import Teacher

from schedule.utils import DateMixin

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


# def create_class(request):
#     if request.method == 'POST':
#         form = ClassFormSet(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/classes')
#         else:
#             print(form.errors)
#     else:
#         form = ClassFormSet()
#
#     context = {
#         'formset': form,
#         'menu_selected': request.path,
#     }
#     return render(request, 'classes/create_class.html', context=context)


def schedule(request):
    print(request.path)
    context = {
        'menu_selected': request.path,
    }
    return render(request, 'main_base.html', context)

# @csrf_exempt
# def delete_subject(request, slug):
#     print(slug)
#     subject = get_object_or_404(Discipline, slug=slug)
#     subject.delete()
#     # return redirect('/subjects')
#     return JsonResponse({'message': 'Object deleted successfully'})
