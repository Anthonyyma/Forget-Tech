from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('favicon.ico/', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.png'))),
]