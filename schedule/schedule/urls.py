"""
URL configuration for schedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('subjects/', subjects),
    path('schedule/', schedule),
    path("__debug__/", include("debug_toolbar.urls")),
    #
    path('export_to_excel/', export_to_excel),
    # path('create_class/', create_class),
    # path('classes/<slug:slug>/update', DetailClass.as_view(), name='class_read'),
    path('classes/<slug:slug>/update', UpdateClass.as_view(), name='class_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.MEDIA_ROOT)

handler404 = page_not_found  # 403, 500
