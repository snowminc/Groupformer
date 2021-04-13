from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import GroupFormer, Participant

def verify_participant(request, group_former_id):
    #attempt to get a group former object, otherwise will return a 404
    group_former = get_object_or_404(GroupFormer, pk=group_former_id)
    try:
     #get the set of participants based on the group former entered
     particpant_obj = group_former.participant_set.get(part_email = request.GET['email'])
    #if the participant doesnt exist, raise a KeyError
    except(KeyError, Participant.DoesNotExist):
        #return code is 200 - since the view is rendered directly
        return render(request, 'dbtools/pdenied.html')
    # return code will be 302 since doing a redirect to the response screen
    return HttpResponseRedirect(reverse('min_iteration2:response_screen'))



