from django.urls import path

from discipline.views import create_subject, DeleteSubject

urlpatterns = [
    path('', create_subject, name='subjects'),
    path('<slug:slug>/delete/', DeleteSubject.as_view(), name='subject_delete'),
]
