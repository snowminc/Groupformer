from django.shortcuts import render

def homepage(request):
    # Display a basic homepage as a "redirect" hub
    return render(request, 'homepage_main/home.html')
