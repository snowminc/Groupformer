from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
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
    return HttpResponseRedirect(reverse('response_screen:response_screen', kwargs={"groupformer_id": group_former.pk}))

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


def record_response(request, group_former_id):
    '''

    :param request:
    :param group_former_id: get the groupformer id from the url
    :return: redirects to the root directory if response is recorded or raises a 404 if the request.METHOD is not a POST
    '''
    if request.method == "POST":
        #get the group former from the id in the url
        gf:GroupFormer = get_object_or_404(GroupFormer, pk=group_former_id)

        #the name of the participant can be retrieved using the key, participantName
        name = request.POST.get("participantNameForm")

        #the email of the participant can be retrieved using the key, participantEmailForm
        email = request.POST.get("participantEmailForm")

        #using the email, get the participant
        part_obj = gf.getParticipantByEmail(email)

        #get all the projects associated with the specific groupformer ID
        projects = Project.objects.filter(group_former=gf)
        #template key from the response screen
        key_template = "projForm#_preference"
        proj_pref_keys = {}
        #loop to get the the project id, the full key, the value for the key, and the project object
        for proj in projects:
            proj_pref_keys[proj.id] = {}
            proj_pref_keys[proj.id]["param_key"] = key_template.replace("#", str(proj.id))
            proj_pref_keys[proj.id]["value"] = int(request.POST.get(proj_pref_keys[proj.id]["param_key"]))
            proj_pref_keys[proj.id]["object"] = proj
            #add the participants project choice
            part_obj.projectChoice(proj_pref_keys[proj.id]["object"], proj_pref_keys[proj.id]["value"])

        #get all the attributes associated with the groupformer
        attributes = Attribute.objects.filter(group_former=gf)
        # template key from the response screen
        key_template = "attrForm#_preference"
        attr_pref_keys = {}
        # loop to get the the attribute id, the full key, the value for the key, and the attribute object
        for attr in attributes:
            attr_pref_keys[attr.id] = {}
            attr_pref_keys[attr.id]["param_key"] = key_template.replace("#", str(attr.id))
            attr_pref_keys[attr.id]["value"] = int(request.POST.get(attr_pref_keys[attr.id]["param_key"]))
            attr_pref_keys[attr.id]["object"] = attr
            #add the participants attribute choice
            part_obj.attributeChoice(attr_pref_keys[attr.id]["object"], attr_pref_keys[attr.id]["value"])

        #get the list of the partners desired partners to work with
        partners = request.POST.getlist("participantForm_preference")
        if(partners is not None):
            for des_name in partners:
                part = gf.getParticipantByName(des_name)
                part_obj.desires(part)

        # redirecting to the root directory, if the request method is POST
        return HttpResponseRedirect("/")

    #returns a 404 if not the appropriate request method
    else:
        raise Http404