from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Project

class IndexView(generic.ListView):
    template_name = 'projects/dropdown_test.html'
    context_object_name = 'projects_list'

    def get_queryset(self):
        return Project.objects.all()
