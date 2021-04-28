from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponse
from django.template import RequestContext
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from dbtools.models import *

def response_screen(request, groupformer_id):
    # Check if the groupformer page exists before accessing
    if GroupFormer.objects.filter(pk=groupformer_id).exists():
        # Get all applicable projects, attributes, and participants to build the response page.
        projects = Project.objects.filter(group_former=groupformer_id)
        attributes = Attribute.objects.filter(group_former=groupformer_id)
        participants = Participant.objects.filter(group_former=groupformer_id)
        context = {"projects": projects, "attributes": attributes, "participants": participants}

        return render(request, 'response_screen_main/response_screen.html', context)

    return HttpResponse("404", status=404)


def login_group(request, groupformer_id):
    gfs = GroupFormer.objects.filter(pk=groupformer_id)
    if len(gfs) == 0:
        return render(request, 'response_screen_main/loginerror.html')
    gf = gfs[0]

    if request.POST.get("email"):
        # Validate the login
        parts = gf.getParticipantByEmail(request.POST["email"])
        if parts == None:
            return render(request, 'response_screen_main/login.html', {"groupformer": gf, 'error': True})
        return redirect(reverse('response_screen:response_screen', kwargs={"groupformer_id": gf.pk}))

    # Log into the groupformer for the first time
    return render(request, 'response_screen_main/login.html', {"groupformer": gf})
