from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from pytils.translit import slugify

from discipline.forms import DisciplineFormSet
from discipline.models import Discipline
from schedule.utils import DateMixin


@csrf_exempt
def create_discipline(request):
    for o in Discipline.objects.all():
        o.slug = slugify(o.name)
        o.save()

    if request.method == 'POST':
        form = DisciplineFormSet(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/disciplines')
        else:
            print(form.errors)
    else:
        form = DisciplineFormSet()

    context = {
        'formset': form,
        'menu_selected': request.path,
    }
    return render(request, 'discipline/all.html', context=context)


class DeleteDiscipline(DateMixin, DeleteView):
    model = Discipline
    template_name = 'discipline/delete.html'
    success_url = reverse_lazy('disciplines')

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

