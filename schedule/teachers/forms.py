from django import forms

from teachers.models import Teacher, Discipline


class AddTeacherForm(forms.ModelForm):
    # subject=forms.ModelMultipleChoiceField(queryset=Discipline.objects.all(), widget=forms.CheckboxSelectMultiple(),empty_label='Ничего не выбрано')

    class Meta:
        model = Teacher
        fields = '__all__'