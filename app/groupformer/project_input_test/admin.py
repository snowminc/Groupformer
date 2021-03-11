from django.contrib import admin

from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Projects', {'fields': ['project_name', 'project_description']}),
    ]
    inlines = []
    list_display = ('project_name', 'project_description')
    list_filter = []
    search_fields = ['project_name']

admin.site.register(Project, ProjectAdmin)