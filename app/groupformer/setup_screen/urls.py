from django.urls import path

from . import views

app_name = 'setup_screen'
urlpatterns = [
    path('dropdown_test', views.dropdown_test, name='dropdown_test'),
    path('', views.index, name='index'),
    path('add_project', views.add_project, name='add_project'), # TODO: remove
    path('remove_project/<int:proj_id>', views.remove_project, name='remove_project'), # TODO: remove
    # TODO: create_groupformer endpoint
]