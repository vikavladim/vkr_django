from django import forms
from django.forms import modelformset_factory, widgets

from teachers.models import Class, Discipline


# class AddClassForm(forms.ModelForm):
#     class Meta:
#         model = Class
#         fields = ['id', 'digit', 'letter']

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ['id', 'name', 'short_name']


# ClassFormSet = modelformset_factory(Class, form=AddClassForm,
#                                     extra=1)
SubjectFormSet = modelformset_factory(Discipline, form=AddSubjectForm,
                                    extra=3)

