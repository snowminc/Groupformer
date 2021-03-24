from django.urls import path

from . import views

app_name = 'form'
urlpatterns = [
    path('dropdown_test', views.index, name='index'),
    path('setup_screen', views.setup_screen, name='setup_screen'),
]