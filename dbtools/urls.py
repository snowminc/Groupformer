from django.urls import path
from . import views

app_name = 'dbtools'
urlpatterns = [
    #example url: {{group_former_id}}/login?email=jules@jules.jules
    path('<int:group_former_id>/login', views.verify_participant, name ='verify_participant'),
    path('', views.project_index, name='project_index'),
    path('<int:group_former_id>/add_project', views.project_create_view, name='add_project'),
    path('<int:group_former_id>/record_response', views.record_response, name='record_response')
]
