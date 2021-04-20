from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import redirect

from dbtools.models import *

def response_screen(request):
    # Create arbitrary sample projects and attributes for testing the front-end
    projects = []
    project = {
        "name": "SomethingProject",
        "description": "Some description about something that has some substance about some of what something entails"
    }
    projects.append(project)
    project = {
        "name": "OtherProject",
        "description": "Some description about something that has some substance about some of what something entails"
    }
    projects.append(project)

    attributes = []
    attribute = {
        "name": "How comfortable are you with front-end?",
    }
    attributes.append(attribute)
    attribute = {
        "name": "How comfortable are you with back-end?",
    }
    attributes.append(attribute)
    return render(request, 'main/response_screen.html', {"projects": projects, "attributes": attributes})

"""
Possible DetailView idea for creating a response for a specific GroupFormer setup.

class FormResponseView(generic.DetailView):
    model = Form
    context_object_name = 'form_details'
    template_name = 'main/response_screen.html'
"""

def groupformer_list(request):
    # Create arbitrary groupformer sections for testing the front-end
    groupformers = []
    groupformers.append({
        "id": 1,
        "section": "Section W"
    })
    groupformers.append({
        "id": 2,
        "section": "Section A"
    })
    return render(request, 'main/groupformer_list.html', {"groupformers": groupformers})

def sample_groups(request, groupformer_id):
    # Create arbitrary sample groups for testing the front-end
    sections = {}

    groups = []
    groups.append(["A","B","C"])
    groups.append(["1","2","3"])
    groups.append(["X","Y","Z"])
    
    sections[1] = groups

    groups = []
    groups.append(["Q","A","Z"])
    groups.append(["G","M","E"])
    groups.append(["A","S","D","F"])

    sections[2] = groups

    if groupformer_id in sections:
        return JsonResponse({"data":sections[groupformer_id]})
    else:
        return JsonResponse({"data":[]}, status=404)