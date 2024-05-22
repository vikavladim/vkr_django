from django.urls import path

from discipline.views import create_subject, DeleteSubject
from level.views import CreateLevel

urlpatterns = [
    path('create/', CreateLevel.as_view(), name='subjects'),
]
