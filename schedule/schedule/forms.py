from django import forms
from django.forms import modelformset_factory

from teachers.models import Class


class AddClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['id', 'digit', 'letter']

ClassFormSet = modelformset_factory(Class, form=AddClassForm,
                                    extra=1)  # Установите extra=0 для отображения форм только существующих объектов
