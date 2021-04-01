from django.test import TestCase
from django.urls import reverse

from .models import Project

# Helper function for ease of Project creation
def create_project(name, description):
    return Project.objects.create(project_name=name, project_description=description)

class ProjectIndexViewTests(TestCase):
    def test_no_projects(self):
        """
        If no Projects exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('project_input_test:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No projects are available.")
        self.assertQuerysetEqual(response.context['projects_list'], [])

    def test_existing_project(self):
        """
        If a Project exists, its name and description is displayed.
        """
        project = create_project("Tester", "A project dedicated to running effective tests.")
        response = self.client.get(reverse('project_input_test:index'))
        self.assertContains(response, project.project_name)
        self.assertContains(response, project.project_description)

class DatabaseTests(TestCase):
    def test_setup(self):
        #Setup a basic structure
        pass
    
    def test_adding(self):
        #Add various additional entities and relationships
        pass
    
    def test_removing(self):
        #Remove different elements and test their outputs
        pass
    
    def test_cleanup(self):
        #Clear database by removing GroupFormers
        pass
