from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *

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
    return HttpResponseRedirect(reverse('results_screen:response_screen'))

# Migrated from projects/

def project_index(request):
    """

    :param request:
    :return: render will re-display the form to submit another project and description
    """
    return render(request, "projects/projects.html")

# view where the form sends the data, accepts the project names and descriptions
def project_create_view(request, group_former_id):
    """
    :param request:
    :return: returns a HttpResponseRedirect after posting the data to prevent the data being stored two times
    """
    
    group_former = get_object_or_404(GroupFormer, pk=group_former_id)
    
    # assuming the front_end is saving what the users enters as project_name and project_description
    try:
        group_former.addProject(request.POST["project_name"], request.POST["project_description"])
    except(ValueError):
        return render(request, 'dbtools/palreadyexists.html')
    #allows it to go back to ask for another project description - index is displaying the page
    #reverse takes the name and looks in urls for the full urls
    #sending them back to the form -> project_index to stay on the same page to ask for another
    # project name and description
    return HttpResponseRedirect(reverse("project_index"))
