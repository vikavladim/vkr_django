from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from level.models import Level
from schedule.utils import DateMixin


class CreateLevel(DateMixin, CreateView):
    model = Level
    template_name = 'grades/create_grade.html'
    context_object_name = 'grade'
    fields = ['name', 'subject']
    success_url = reverse_lazy('classes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Создание параллели',
            menu_selected=self.request.path,
            **kwargs
        )
