from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.FilteredCarAdTest.as_view(), name='dashboard'),
]
