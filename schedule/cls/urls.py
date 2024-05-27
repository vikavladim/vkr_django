from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:slug>/update/', UpdateClass.as_view(), name='class_update'),
    path('<slug:slug>/update/', UpdateClass.as_view(), name='class_update'),
    path('', class_list, name='classes'),
    path('create_class', CreateClass.as_view(), name='create_class'),
    path('create_level/', CreateLevel.as_view(), name='create_level'),
    path('getTeachersFromDB/', getTeachersFromDB, name='getTeachersFromDB'),
    path('getHoursFromDB/', getHoursFromDB, name='getHoursFromDB'),
    path('teachers_field_form/', teachers_field_form, name='teachers_field_form'),
    path('load_field_form/', load_field_form, name='load_field_form'),
    path('<slug:slug>/delete/', DeleteClass.as_view(), name='class_delete'),
]
