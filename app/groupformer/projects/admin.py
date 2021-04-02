from django.contrib import admin

# Register the Project Model on the admin site
from .models import Project

admin.site.register(Project)
