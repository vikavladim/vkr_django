from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView

from schedule import settings
from schedule.views import *

from teachers.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('home/', HomeView.as_view(), name='home'),
    path('teachers/', include('teachers.urls')),
    path('classes/', include('cls.urls')),
    path('programs/', include('program.urls')),
    path('disciplines/', include('discipline.urls')),
    path('schedule/', schedule),
    path("__debug__/", include("debug_toolbar.urls")),
    path('export_to_excel/', export_to_excel),
  ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found  # 403, 500
