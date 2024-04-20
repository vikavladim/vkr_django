from django.contrib import admin
from django.urls import path, include

from teachers.views import *

urlpatterns = [
    path('', TeacherListView.as_view(), name='teachers'),
    path('create/', AddTeacher.as_view(), name='teacher_create'),
    # path('<slug:slug>/read', DetailTeacher.as_view(), name='teacher_read'),
    path('<slug:slug>/update', UpdateTeacher.as_view(), name='teacher_update'),
    path('<int:id>/delete', delete, name='teacher_delete'),
    #
    path('getDataFromDB/', getDataFromDB, name='getDataFromDB'),
]
