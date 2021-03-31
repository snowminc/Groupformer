from django.urls import path

from . import views

app_name = 'setup_screen'
urlpatterns = [
    path('dropdown_test', views.dropdown_test, name='dropdown_test'),
    path('', views.index, name='index'),
    # TODO: create_groupformer endpoint
]