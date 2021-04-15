from django.urls import path

from . import views

app_name = 'min_iteration3'
urlpatterns = [
    path('response_screen/<int:groupformer_id>', views.response_screen, name='response_screen'),
    path('groupformer_list/', views.groupformer_list, name='groupformer_list'),
    path('groupformer_list/sample_groups/<int:groupformer_id>', views.sample_groups, name='sample_groups'),
]