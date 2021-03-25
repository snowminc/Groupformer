from django.http import HttpResponse
from django.shortcuts import render

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


def index(request):

    if 'setup_projects' not in request.session: # doesn't exist, so add single blank project
        request.session['setup_projects'] = [
            {
                "name": "",
                "description": "",
            },
        ]


    context = {}

    context["projects"] = request.session['setup_projects']

    return render(request, "setup_screen/setup_screen.html", context=context)


def add_project(request):
    request.session['setup_projects'].append({
                "name": "",
                "description": "",
            },)

    return setup_screen(request)
