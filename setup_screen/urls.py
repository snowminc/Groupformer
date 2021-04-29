from django.urls import path

from . import views

app_name = 'setup_screen'
urlpatterns = [
    path('dropdown_test', views.dropdown_test, name='dropdown_test'),
    path('', views.index, name='index'),
    path('submit_groupformer', views.submit_groupformer, name='submit_groupformer'),
    path('login_screen', views.login_screen, name='login_screen'),
    path('login_endpoint', views.login_endpoint, name='login_endpoint'),
    path('logout_endpoint', views.logout_endpoint, name='logout_endpoint'),
    path('create_account', views.create_account, name='create_account'),
]
