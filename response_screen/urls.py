from django.urls import path

from . import views

app_name = 'response_screen'
urlpatterns = [
    path('<int:groupformer_id>', views.response_screen, name='response_screen'),
    path('groupformer_list/', views.groupformer_list, name='groupformer_list'),
    path('groupformer_list/sample_groups/<int:groupformer_id>', views.sample_groups, name='sample_groups'),
    path('<int:groupformer_id>/login', views.login_group, name='login')
]
