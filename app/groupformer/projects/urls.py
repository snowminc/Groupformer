
from django.urls import path
from . import views
urlpatterns = [
    path('', views.project_index, name='project_index'),
    path('add_project', views.project_create_view, name='add_project'),
]