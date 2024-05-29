import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView

from discipline.models import Discipline
from program.models import ProgramDisciplines, Program
from schedule.utils import DateMixin


def programs(request):
    # classes = Class.objects.all()
    programs = Program.objects.all()
    students = {}

    for program in programs:
        if program.digit not in students:
            students[program.digit] = []
        students[program.digit].append(program)

    context = {
        'title': 'Классы',
        'students': students,
        'menu_selected': request.path,
    }

    return render(request, 'program/program_list.html', context)


class CreateProgram(DateMixin, CreateView):
    model = Program
    template_name = 'program/create_program.html'
    context_object_name = 'Program'
    fields = ['digit', 'name', ]
    success_url = reverse_lazy('programs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Создание параллели',
            all_disciplines=Discipline.objects.all(),
            menu_selected=self.request.path,
            **kwargs
        )


def getHoursFromDB(request):
    selected_values = request.GET.getlist('selectedValues[]')
    obj_id = request.GET.get('programId')
    if obj_id:
        obj = get_object_or_404(Program, id=obj_id)
    else:
        obj = Program.objects.last()
    # obj = Program.objects.filter(id=obj_id).first()
    # obj = get_object_or_404(Program, id=obj_id)

    hours_by_disciplines = {'array': [], }

    for selectedValue in selected_values:
        discipline = get_object_or_404(Discipline, id=selectedValue)
        load = ProgramDisciplines.objects.filter(program=obj, discipline=discipline).first()

        discipline_data = {
            'discipline': discipline.serializable,
            'load': load.load if load else 1
        }

        hours_by_disciplines['array'].append(discipline_data)

    return JsonResponse(hours_by_disciplines)


@csrf_exempt
def load_field_form(request):
    print('hell0')
    if request.method == 'POST':
        data = json.loads(request.body)
        disciplines_array = data.get('array')
        program_id = data.get('id')
        program_name = data.get('program_name')
        digit = data.get('digit')

        if program_id:
            program = get_object_or_404(Program, id=program_id)
            program.digit = digit
            program.name = program_name
            program.save()

            old_disciplines = ProgramDisciplines.objects.filter(program=program)

            for discipline in disciplines_array:
                dis = get_object_or_404(Discipline, id=discipline['id_discipline'])
                program_obj = ProgramDisciplines.objects.filter(program=program, discipline=dis).first()

                if program_obj:
                    program_obj.load = discipline['load']
                    program_obj.save()
                    old_disciplines = old_disciplines.exclude(id=program_obj.id)
                else:
                    ProgramDisciplines.objects.create(program=program, discipline=dis, load=discipline['load'])

            deleted_ids = [obj.id for obj in old_disciplines]
            ProgramDisciplines.objects.filter(id__in=deleted_ids).delete()

        else:
            program = Program.objects.create(digit=digit, name=program_name)
            # program, _ = Program.objects.get_or_create(digit=digit, name=program_name)
            for discipline in disciplines_array:
                dis = get_object_or_404(Discipline, id=discipline['id_discipline'])

                program_obj = ProgramDisciplines.objects.create(program=program, discipline=dis,
                                                                load=discipline['load'])
                # program_obj, _ = ProgramDisciplines.objects.get_or_create(program=program, discipline=dis,
                #                                                           load=discipline['load'])
                program_obj.load = discipline['load']
                program_obj.save()

    return redirect('programs')


class UpdateProgram(DateMixin, UpdateView):
    model = Program
    template_name = 'program/create_program.html'
    # context_object_name = 'program'
    fields = ['digit', 'name', ]
    success_url = reverse_lazy('programs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = self.get_object()

        all_disciplines = Discipline.objects.all()
        # select_disciplines = ProgramDisciplines.objects.filter(program=program)
        select_disciplines_ids = ProgramDisciplines.objects.filter(program=program).values_list('discipline_id',
                                                                                                flat=True)
        # print(all_disciplines, select_disciplines_ids)


        return self.get_mixin_context(
            context,
            title='Создание параллели',
            all_disciplines=Discipline.objects.all(),
            # select_disciplines=select_disciplines,
            select_disciplines_ids=ProgramDisciplines.objects.filter(program=program).values_list('discipline_id',
                                                                                             flat=True),
            menu_selected=self.request.path,
            **kwargs
        )
