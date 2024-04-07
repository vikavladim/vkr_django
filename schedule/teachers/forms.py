from django import forms
from pytils.templatetags.pytils_translit import slugify

from teachers.models import Teacher, Discipline


class AddTeacherForm(forms.ModelForm):
    # subject=forms.ModelMultipleChoiceField(queryset=Discipline.objects.all(), widget=forms.CheckboxSelectMultiple(),empty_label='Ничего не выбрано')

    class Meta:
        model = Teacher
        fields = ['fio','slug','photo','room','subject']
        # fields = '__all__'
        # prepopulated_fields = {'slug': ('fio',)}

    # def save(self, commit=True):
    #     teacher = super().save(commit=False)
    #     teacher.slug = slugify(teacher.fio)
    #     if commit:
    #         teacher.save()
    #     return teacher

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.fio)
    #     super().save()