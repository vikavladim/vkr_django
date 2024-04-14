from django import forms
from django.forms import modelformset_factory, widgets

from teachers.models import Class, Discipline


class AddClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['id', 'digit', 'letter']


ClassFormSet = modelformset_factory(Class, form=AddClassForm,
                                    extra=1)  # Установите extra=0 для отображения форм только существующих объектов


# class UpdateClassForm(forms.ModelForm):
#     linked_bars = forms.ModelMultipleChoiceField(queryset=Discipline.objects.all(),
#                                                  widget=widgets.SelectMultiple(
#                                                      Discipline._meta.verbose_name_plural,
#                                                      False),attrs={'class': 'Discipline'})
#
#     class Meta:
#         model = Class
#         fields = ['letter', 'slug', 'digit', 'subject', 'linked_bars']
#         # widgets = {
#         #     'subject': forms.SelectMultiple(attrs={'class': 'filter_horizontal'}),
#         # }
