from django.test import TestCase
from django.urls import reverse


class HomeViewTest(TestCase):

    def test_setup_screen_link(self):
        """
        Ensure the link to the setup screen is included
        """
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'href="{}"'.format(reverse('setup_screen:index')))

    def test_page_load(self):
        """
        Ensure the general page information (non-link) loaded
        """
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, "If you are the one organizing the groups, click the button below and log in if you haven't already.")
