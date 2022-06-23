from django.contrib import admin
from django.urls import path

from django_ex_1.apps.main.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view())
]
