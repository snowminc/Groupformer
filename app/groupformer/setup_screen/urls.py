from django.urls import path

from . import views

app_name = 'setup_screen'
urlpatterns = [
    path('dropdown_test', views.dropdown_test, name='dropdown_test'),
    path('', views.index, name='index'),
    path('submit_groupformer', views.submit_groupformer, name='submit_groupformer'),
]