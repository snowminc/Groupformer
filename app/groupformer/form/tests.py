from django.test import TestCase
from django.urls import reverse


class ParticipantDropdownViewTests(TestCase):

    def test_participant_dropdown(self):
        """
        Ensure the participant dropdown exists
        NOTE: this test will break and will need to be changed once we have actual data from the models
        """
        response = self.client.get(reverse('form:index'))
        print(response)
        self.assertContains(response, '<select name="participants"')
        self.assertContains(response, 'Min Chon')
