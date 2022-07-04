from django.contrib import admin
from django.urls import path, include

from django_ex_1.apps.main.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),

    path('', IndexView.as_view(), name='index'),
]
