from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import redirect

from dbtools.models import *
from prio_alg.priority import calc_optimal_groups

"""
Possible DetailView idea for creating a response for a specific GroupFormer setup.

class FormResponseView(generic.DetailView):
    model = Form
    context_object_name = 'form_details'
    template_name = 'results_screen_main/response_screen.html'
"""

def results_screen(request):
    if not request.user.is_authenticated:
        return redirect(reverse('setup_screen:login_screen') + '?redirect=results_screen')

    # Get all groupformers to list groupformer instances for group generating
    groupformers = GroupFormer.objects.all()
    context = {"groupformers": groupformers}

    return render(request, 'results_screen_main/results_screen.html', context)


def get_groups(request, groupformer_id):
    groupformer = GroupFormer.objects.get(pk=groupformer_id)
    best_groups, second_groups, third_groups = calc_optimal_groups(groupformer, max_parts=groupformer.max_participants_per_group, epoch=400)
    
    payload = {}
    for group in best_groups[0]:
        project_name = group[0].project_name
        participants = group[1]

        payload[project_name] = []
        for p in participants:
            payload[project_name].append(p.part_name)

    """
    Format:
        {
            "name1": [
                "pname1",
                "pname2",
                "pname3"
            ],
            "name2"; [
                "pname4",
                "pname5",
                "pname6"
            ]
        }
    """

    return JsonResponse({"data": payload})