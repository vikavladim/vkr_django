from django.urls import path
from .views import *

urlpatterns = [
    path('', programs, name='programs'),
    path('create_program/', CreateProgram.as_view(), name='create_program'),
    path('<slug:slug>/update', UpdateProgram.as_view(), name='update_program'),
    path('getHoursFromDB/', getHoursFromDB, name='getHoursFromDB'),
    path('load_field_form/', load_field_form, name='load_field_form'),
]
