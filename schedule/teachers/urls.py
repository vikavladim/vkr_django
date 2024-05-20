from django.contrib import admin
from django.urls import path, include

from teachers.views import *

urlpatterns = [
    path('', TeacherListView.as_view(), name='teachers'),
    path('create/', AddTeacher.as_view(), name='teacher_create'),
    # path('<slug:slug>/read', DetailTeacher.as_view(), name='teacher_read'),
    path('<slug:slug>/update', UpdateTeacher.as_view(), name='teacher_update'),
    # path('<slug:slug>/delete', delete, name='teacher_delete'),
    path('<slug:slug>/delete', DeleteTeacher.as_view(), name='teacher_delete'),
    #
    path('getDataFromDB/', getDataFromDB, name='getDataFromDB'),
    path('classes_field_form/', classes_field_form, name='classes_field_form'),
]
