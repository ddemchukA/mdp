from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    re_path(r'^contacts', views.contacts, name='contacts'),
]