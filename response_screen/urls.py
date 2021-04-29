from django.urls import path

from . import views

app_name = 'response_screen'
urlpatterns = [
    path('<int:groupformer_id>', views.response_screen, name='response_screen'),
    path('<int:groupformer_id>/login', views.login_group, name='login'),
    path('<int:groupformer_id>/logout', views.logout, name='logout'),
    path('submit', views.temporary_submit_test, name='temporary_submit_test')
]
