from django.urls import path
from . import views

urlpatterns = [
    #example url: {{group_former_id}}/login?email=jules@jules.jules
    path('<int:group_former_id>/login/', views.verify_participant, name = 'verify_participant'),
]