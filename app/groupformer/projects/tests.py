from django.test import TestCase
from django.urls import reverse
from projects.models import Project

class ProjectModelTests(TestCase):
    #test to set up the test functions by adding Project Objects into the "test" database
    def setUp(self):
        Project.add_project("Test 1", "Test 1 Description")
        Project.add_project("Test 2", "Test 2 Description")
        Project.add_project("Test 3", "Test 3 Description")
        Project.add_project("Test 4", "Test 4 Description")

    #test to see if the first object in the database is correct
    def test_first_project(self):
        project_obj = Project.objects.all()[0]
        self.assertEqual(project_obj.project_name, "Test 1")
        self.assertEqual(project_obj.project_description, "Test 1 Description")

    #test to see if the last object in the database is correct
    def test_last_project(self):
        project_obj = Project.objects.last()
        self.assertEqual(project_obj.project_name, "Test 4")
        self.assertEqual(project_obj.project_description, "Test 4 Description")

    #test to make sure the view properly saved the database
    def test_project_saved(self):
        project_objects_dict = {"project_name": "Test 1", "project_description": "Test Description"}
        response = self.client.post(reverse('add_project'), project_objects_dict)
        # response code for redirecting is 302
        self.assertEqual(response.status_code, 302)
        #checking the first project object
        project_obj = Project.objects.all()[0]
        self.assertEqual(project_obj.project_name, "Test 1")


