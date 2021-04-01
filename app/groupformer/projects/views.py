from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Project
# Create your views here.

# view to render/display the form
def project_index(request):
    return render(request, "projects/projects.html")

# view where the form sends the data, accepts the project names and descriptions
def project_create_view(request):
    """
    :param request:
    :return:
    """
    # assuming the front_end is saving what the users enters as project_name and project_description
    Project.add_project(request.POST["project_name"], request.POST["project_description"])
    #allows it to go back to ask for another project description - index is displaying the page
    #reverse takes the name and looks in urls for the full urls
    #sending them back to the form -> project_index to stay on the same page to ask for another
    # project name and description
    return HttpResponseRedirect(reverse("project_index"))
