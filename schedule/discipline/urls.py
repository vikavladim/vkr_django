from django.urls import path

from discipline.views import create_discipline, DeleteDiscipline

urlpatterns = [
    path('', create_discipline, name='disciplines'),
    path('<slug:slug>/delete/', DeleteDiscipline.as_view(), name='discipline_delete'),
]
