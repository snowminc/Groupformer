from django.urls import path

from . import views

app_name = 'results_screen'
urlpatterns = [
    path('', views.groupformer_list, name='results_screen'),
    path('sample_groups/<int:groupformer_id>', views.sample_groups, name='sample_groups'),
]
