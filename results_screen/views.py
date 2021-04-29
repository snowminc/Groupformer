from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import redirect

from dbtools.models import *

"""
Possible DetailView idea for creating a response for a specific GroupFormer setup.

class FormResponseView(generic.DetailView):
    model = Form
    context_object_name = 'form_details'
    template_name = 'results_screen_main/response_screen.html'
"""

def groupformer_list(request):

    # page requires login
    if not request.user.is_authenticated:
        return redirect(reverse('setup_screen:login_screen') + '?redirect=results_screen')

    #TODO: filter groupformers by user email
    #TODO: probably will want to associate groupformers to the actual user object (not just email)

    # Get all groupformers to list groupformer instances for group generating
    groupformers = GroupFormer.objects.all()
    context = {"groupformers": groupformers}

    return render(request, 'results_screen_main/groupformer_list.html', context)


def sample_groups(request, groupformer_id):
    # Temporary "API endpoint" for retrieving groups
    # Create arbitrary sample groups for testing the front-end
    sections = {}

    # Even ids
    groups = []
    groups.append(["A", "B", "C"])
    groups.append(["1", "2", "3"])
    groups.append(["X", "Y", "Z"])

    sections[0] = groups

    # Odd ids
    groups = []
    groups.append(["Q", "A", "Z"])
    groups.append(["G", "M", "E"])
    groups.append(["A", "S", "D", "F"])

    sections[1] = groups

    # Subtract 1 to group former ID because ABC is on even ids, and PKs count from 1
    if (groupformer_id - 1) % 2 in sections:
        return JsonResponse({"data": sections[(groupformer_id - 1) % 2]})
    else:
        return JsonResponse({"data": []}, status=404)