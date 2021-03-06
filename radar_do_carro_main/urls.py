from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('criar_conta', views.criar_conta, name='criar_conta'),
    path('login/', auth_views.LoginView.as_view(template_name='radar_do_carro_main/login.html')),
    path('logout/', views.logout_view),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    re_path(r'^go_to_ad/(?P<ad_id>[0-9A-Za-z._-]+)/$', views.go_to_ad, name='go_to_ad'),
    re_path(r'^dashboard/$', views.dashboard, name='dashboard'),
    re_path(r'^dashboard/(?P<marca_modelo>[0-9A-Za-z._-]+)/$', views.dashboard, name='dashboard'),
    re_path(r'^fipe/$', views.fipe, name='fipe'),
    re_path(r'^fipe/(?P<marca_modelo>[0-9A-Za-z._-]+)/$', views.fipe, name='fipe'),
]
