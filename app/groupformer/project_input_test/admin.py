from django.contrib import admin

from .models import *

class GroupFormerAdmin(admin.ModelAdmin):
    search_fields = ['class_section']

class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['project_name']

class AttributeAdmin(admin.ModelAdmin):
    pass

class ParticipantAdmin(admin.ModelAdmin):
    pass

class AttrChoiceAdmin(admin.ModelAdmin):
    pass

class ProjChoiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(GroupFormer, GroupFormerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(attribute_selection, AttrChoiceAdmin)
admin.site.register(project_selection, ProjChoiceAdmin)
