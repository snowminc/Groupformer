from django.db import models

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=240, blank=False, null=False)
    project_description = models.TextField(blank=False, null=False)

    # model function to add a project name and project description
    def add_project(name, description):
        """
        :param name, description:
        :return: the project object that has been added to the database
        """
        proj = Project(project_name = name, project_description = description)
        proj.save()
        return proj


