from django.urls import path
from . import views

urlpatterns = [

    #/response_screen/{{group_former_id}}/login?email="jules@jules.jules"
    path('<int:group_former_id>/login/<string:email>/', views.verify_participant, name = 'verify_participant'),
]