from django.urls import re_path

from . import views

urlpatterns = [
    #path('dashboard/', views.FilteredCarAdTest.as_view(), name='dashboard'),
    re_path(r'^dashboard/$', views.dashboard, name='dashboard'),
    re_path(r'^dashboard/(?P<marca_modelo>[0-9A-Za-z._-]+)/$', views.dashboard, name='dashboard'),
]
