from django.test import TestCase
from django.urls import reverse


class MinIteration2ResponseScreenTests(TestCase):
    def test_displays_all_projects(self):
        """
        If the page shows all of the arbitrary project inputs (without backend) from views.py, then it passes
        """
        response = self.client.get(reverse('min_iteration2:response_screen'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SomethingProject")
        self.assertContains(response, "OtherProject")
        self.assertContains(response, "Some description about something that has some substance about some of what something entails")

    def test_displays_all_attributes(self):
        """
        If the page shows all of the arbitrary attribute inputs (without backend) from views.py, then it passes
        """
        response = self.client.get(reverse('min_iteration2:response_screen'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How comfortable are you with front-end?")
        self.assertContains(response, "How comfortable are you with back-end?")