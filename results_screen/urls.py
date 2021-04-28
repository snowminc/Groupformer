from django.urls import path

from . import views

app_name = 'results_screen'
urlpatterns = [
    path('groupformer_list/', views.groupformer_list, name='groupformer_list'),
    path('groupformer_list/sample_groups/<int:groupformer_id>', views.sample_groups, name='sample_groups'),
]