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

# TODO: submit groupformer endpoint to commit projects/attributes to database