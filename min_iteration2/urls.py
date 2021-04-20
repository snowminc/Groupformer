from django.urls import path

from . import views

app_name = 'min_iteration2'
urlpatterns = [
    path('response_screen/', views.response_screen, name='response_screen'),
    #path('response_screen/<int:pk>/', views.FormResponseView.as_view(), name='form_response')  Idea for using Form as a model for DetailView
    
    path('groupformer_list/', views.groupformer_list, name='groupformer_list'),
    path('groupformer_list/sample_groups/<int:groupformer_id>', views.sample_groups, name='sample_groups'),
]
