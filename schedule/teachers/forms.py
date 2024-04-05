from django import forms

from teachers.models import Teacher


class AddTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'