import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from dbtools.models import *


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

    if not request.user.is_authenticated:
        return redirect(reverse('setup_screen:login_screen'))

    context = {}

    return render(request, "setup_screen/setup_screen.html", context=context)


def submit_groupformer(request):
    if request.is_ajax():
        if request.method == 'POST':
            print('Raw Data: "%s"' % request.body)
            payload = json.loads(request.body)

            # Create a new groupformer instance
            instructor_name = payload["instructor_name"]
            instructor_email = payload["instructor_email"]
            custom_name = payload["custom_name"]
            people_per_group = payload["people_per_group"]  # TODO: people_per_group
            gf = addGroupFormer(instructor_name, instructor_email, custom_name)

            # add participants to the groupformer
            addRoster(gf, payload["participant_roster"])

            # add projects
            for project_data in payload["projects"]:
                project_name = project_data["name"]
                project_description = project_data["description"]
                addProject(gf, project_name, project_description)

            # add attributes
            for attribute_data in payload["attributes"]:
                attribute_name = attribute_data["name"]
                attribute_homogenous = attribute_data["is_homogenous"]
                addAttribute(gf, attribute_name, attribute_homogenous, False)

    return HttpResponse("OK")


def login_screen(request):
    redirect_value = ""
    if 'redirect' in request.GET:
        redirect_value = request.GET['redirect']

    if request.user.is_authenticated:
        if redirect_value == 'results_screen':
            return redirect(reverse('results_screen:results_screen'))
        return redirect(reverse('setup_screen:index'))

    # display login screen
    return render(request,
                  'setup_screen/instructor_login.html',
                  context={'create_account': False, 'redirect': redirect_value}
                  )


def create_account_screen(request):
    redirect_value = ""
    if 'redirect' in request.GET:
        redirect_value = request.GET['redirect']

    if request.user.is_authenticated:
        if redirect_value == 'results_screen':
            return redirect(reverse('results_screen:results_screen'))
        return redirect(reverse('setup_screen:index'))

    # display login screen
    return render(request, 'setup_screen/instructor_login.html', context={'create_account': True})


def login_endpoint(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    redirect_value = ""
    if 'redirect' in request.POST:
        redirect_value = request.POST['redirect']

    if user is not None:
        login(request, user)
        if redirect_value == 'results_screen':
            return redirect(reverse('results_screen:results_screen'))
        return redirect(reverse('setup_screen:index'))

    # failed to authenticate, so display error message
    return render(request, 'setup_screen/instructor_login.html',
                  {
                      'error': 'Could not authenticate user',
                      'create_account': False,
                      'redirect': redirect_value
                  })


def create_account(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    # TODO: create account should not render a new page (b/c we want to preserve the user's input)
    # TODO: should be an ajax request instead

    if password != confirm_password:
        return render(request, 'setup_screen/instructor_login.html',
                      {
                          'error': 'Passwords do not match!',
                          'create_account': True
                      })

    if len(password) < 6:
        return render(request, 'setup_screen/instructor_login.html',
                      {
                          'error': 'Password must be 6 or more characters!',
                          'create_account': True
                      })

    if len(User.objects.filter(username=username)) > 0:
        return render(request, 'setup_screen/instructor_login.html',
                      {
                          'error': 'Username already taken!',
                          'create_account': True
                      })

    if len(User.objects.filter(email=email)) > 0:
        return render(request, 'setup_screen/instructor_login.html',
                      {
                          'error': 'Email already taken!',
                          'create_account': True
                      })

    user: User = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save()

    # redirect to setup screen
    return redirect(reverse('setup_screen:login_screen'))


def logout_endpoint(request):
    logout(request)

    return render(request, 'setup_screen/instructor_login.html',
                  {
                      'success': 'Logged out successfully!',
                      'create_account': False
                  })
