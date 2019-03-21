from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    #path('dashboard/', views.FilteredCarAdTest.as_view(), name='dashboard'),
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='radar_do_carro_main/login.html')),
    path('logout/', views.logout_view),
    re_path(r'^dashboard/$', views.dashboard, name='dashboard'),
    re_path(r'^dashboard/(?P<marca_modelo>[0-9A-Za-z._-]+)/$', views.dashboard, name='dashboard'),
]
