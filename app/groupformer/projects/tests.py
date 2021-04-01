from django.test import TestCase
from .models import Project

class ProjectModelTests(TestCase):
    def test_get_first_project(self):
        project_obj = Project.objects.first()
        self.assertEqual(project_obj.project_name, "Group Former")

    # def test_get_last_project(self):
    #     project_obj = Project.objects.last()
    #     print('Project Name: ', project_obj.project_name, '\n')
    #     print('Project Description: ', project_obj.project_description, '\n')
    #
    # def test_print_all_objects(self):
    #     for project in Project.objects.all():
    #         print('Project Name: ', project.project_name, '\n')
    #         print('Project Description: ', project.project_description, '\n')



