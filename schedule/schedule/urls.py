# from django.conf.urls import handler500
from django.contrib import admin
# from django.template.context_processors import static
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView

# import settings
from schedule import settings
from schedule.views import *

from teachers.views import *  # page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('home/', HomeView.as_view(), name='home'),
    path('teachers/', include('teachers.urls')),
    path('classes/', create_class, name='classes'),
    path('subjects/', create_subject, name='subjects'),
    path('schedule/', schedule),
    path("__debug__/", include("debug_toolbar.urls")),
    #
    path('export_to_excel/', export_to_excel),
    # path('create_class/', create_class),
    # path('classes/<slug:slug>/update', DetailClass.as_view(), name='class_read'),
    path('classes/<slug:slug>/update/', UpdateClass.as_view(), name='class_update'),
    path('classes/getTeachersFromDB/', getTeachersFromDB, name='getTeachersFromDB'),
    path('classes/teachers_field_form/', teachers_field_form, name='teachers_field_form'),
    # path('subjects/<slug:slug>/delete/', DeleteSubject.as_view(), name='subject_delete'),
    path('subjects/<slug:slug>/delete/', delete_subject, name='subject_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.MEDIA_ROOT)

handler404 = page_not_found  # 403, 500
