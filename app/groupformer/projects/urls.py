
from django.urls import path
from . import views
#url pattern for displaying the form
#url pattern for saving what is contained in the form
urlpatterns = [
    path('', views.project_index, name='project_index'),
    path('add_project', views.project_create_view, name='add_project'),
]