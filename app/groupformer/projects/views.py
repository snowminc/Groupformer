from django.shortcuts import render
from .models import Project
# Create your views here.
def project_create_view(request):
    context = {}
    return render(request, "projects/projects.html", context)