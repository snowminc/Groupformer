from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.template import RequestContext
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import *

def response_screen(request, groupformer_id):
    # Check if the groupformer page exists before accessing
    if GroupFormer.objects.filter(pk=groupformer_id).exists():
        # Get all applicable projects, attributes, and participants to build the response page.
        projects = Project.objects.filter(group_former=groupformer_id)
        attributes = Attribute.objects.filter(group_former=groupformer_id)
        participants = Participant.objects.filter(group_former=groupformer_id)
        context = {"projects": projects, "attributes": attributes, "participants": participants}

        return render(request, 'min_iteration3_main/response_screen.html', context)

    return HttpResponse("404", status=404)


def groupformer_list(request):
    # Get all groupformers to list groupformer instances for group generating
    groupformers = GroupFormer.objects.all()
    context = {"groupformers": groupformers}

    return render(request, 'min_iteration3_main/groupformer_list.html', context)


def sample_groups(request, groupformer_id):
    # Temporary "API endpoint" for retrieving groups
    # Create arbitrary sample groups for testing the front-end
    sections = {}

    # Even ids
    groups = []
    groups.append(["A","B","C"])
    groups.append(["1","2","3"])
    groups.append(["X","Y","Z"])
    
    sections[0] = groups

    # Odd ids
    groups = []
    groups.append(["Q","A","Z"])
    groups.append(["G","M","E"])
    groups.append(["A","S","D","F"])

    sections[1] = groups

    # Subtract 1 to group former ID because ABC is on even ids, and PKs count from 1
    if (groupformer_id - 1) % 2 in sections:
        return JsonResponse({"data":sections[(groupformer_id - 1) % 2]})
    else:
        return JsonResponse({"data":[]}, status=404)