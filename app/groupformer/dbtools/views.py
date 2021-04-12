from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import GroupFormer, Participant

def verify_participant(request, group_former_id):
    group_former = get_object_or_404(GroupFormer, pk=group_former_id)
    try:
     particpant_obj = group_former.participant_set.filter(part_email = request.GET['email'])
    except(KeyError, Participant.DoesNotExist):
        return render(request, 'dbtools/pdenied.html')
    return HttpResponseRedirect(reverse('min_iteration2:response_screen'))



