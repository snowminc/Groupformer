from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.


def dropdown_test(request):
    context = {}

    context["participants"] = [
        {"name": "Sarah Nakhon"},
        {"name": "Morgan Vanderhei"},
        {"name": "Kyle Morgan"},
        {"name": "Min Chon"},
        {"name": "Kristian Mischke"}
    ]

    return render(request, "setup_screen/dropdown_test.html", context=context)


def init(request):
    """
    Initialize the session persistent data if it doesn't exist
    """
    if 'setup_projects' not in request.session:  # doesn't exist, so add single blank project
        request.session['setup_projects'] = [
            {
                "name": "",
                "description": "",
            },
        ]


def index(request):
    """
    Setup screen index page. Passes the session data to the html template
    """
    init(request)

    context = {}

    context["projects"] = request.session['setup_projects']

    return render(request, "setup_screen/setup_screen.html", context=context)


def add_project(request):
    """
    Endpoint that adds another blank project to the session data then redirects to the index page
    """
    init(request)

    project_list = request.session['setup_projects']
    project_list.append({
            "name": "",
            "description": "",
        },)
    request.session['setup_project'] = project_list

    return redirect('setup_screen:index')


def remove_project(request, proj_id):
    """
    Endpoint that adds another blank project to the session data then redirects to the index page
    """
    init(request)

    project_list = request.session['setup_projects']
    project_list.append({
            "name": "",
            "description": "",
        },)
    request.session['setup_project'] = project_list

    return redirect('setup_screen:index')