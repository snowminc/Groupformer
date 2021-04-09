import json

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


def index(request):
    """
    Setup screen index page. Passes the session data to the html template
    """

    context = {}

    return render(request, "setup_screen/setup_screen.html", context=context)


def submit_groupformer(request):
    if request.is_ajax():
        if request.method == 'POST':
            print('Raw Data: "%s"' % request.body)
            payload = json.loads(request.body)

            # TODO: create a new groupformer instance
            instructor_name = payload["instructor_name"]
            instructor_email = payload["instructor_email"]
            custom_name = payload["custom_name"]

            for project_data in payload["projects"]:
                project_name = project_data["name"]
                project_description = project_data["description"]
                # TODO: create new project instance in database
                # TODO: link to groupformer instance

            for attribute_data in payload["attributes"]:
                attribute_name = attribute_data["name"]
                attribute_homogenous = attribute_data["is_homogenous"]
                # TODO: create new attribute instance in database
                # TODO: link to groupformer instance
    return HttpResponse("OK")
