from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    context = {}

    context["participants"] = [
        {"name": "Sarah Nakhon"},
        {"name": "Morgan Vanderhei"},
        {"name": "Kyle Morgan"},
        {"name": "Min Chon"},
        {"name": "Kristian Mischke"}
    ]

    return render(request, "form/index.html", context=context)


def setup_screen(request):

    if 'setup_projects' not in request.session: # doesn't exist, so add single blank project
        request.session['setup_projects'] = [
            {
                "name": "",
                "description": "",
            },
        ]


    context = {}

    context["projects"] = request.session['setup_projects']

    return render(request, "form/setup_screen.html", context=context)
