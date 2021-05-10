from django.urls import path

from . import views

app_name = 'results_screen'
urlpatterns = [
    path('', views.results_screen, name='results_screen'),
    path('get_groups/<int:groupformer_id>', views.get_groups, name='get_groups'),
]
