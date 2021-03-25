from django.test import TestCase
from django.urls import reverse


class ParticipantDropdownViewTests(TestCase):

    def test_participant_dropdown(self):
        """
        Ensure the participant dropdown exists
        NOTE: this test will break and will need to be changed once we have actual data from the models
        """
        response = self.client.get(reverse('setup_screen:dropdown_test'))
        self.assertContains(response, '<select name="participants"')
        self.assertContains(response, 'Min Chon')


class SetupScreenTests(TestCase):

    def test_single_project_inputs_exist(self):
        """
        Ensure that a single project input exists when first loading the setup screen page
        """
        response = self.client.get(reverse('setup_screen:index'))
        self.assertContains(response, 'project-name1')
        self.assertContains(response, 'project-desc1')
        self.assertNotContains(response, 'project-name2')
        self.assertNotContains(response, 'project-desc2')

    def test_add_projects_inputs_exist(self):
        """
        Ensure that the add project endpoint adds a new project to the session to be displayed on the setup screen
        """
        for i in range(1, 10):
            response = self.client.get(reverse('setup_screen:add_project'))

            self.assertEqual(response.status_code, 302)  # assert redirecting
            response = self.client.get(reverse('setup_screen:index'))

            for j in range(1, i+1):
                self.assertContains(response, f'project-name{j}')
                self.assertContains(response, f'project-desc{j}')

    def test_add_project_before_visit_index(self):
        """
        Regression Test: Ensure that going to the add project url is okay to do before going to the index.
        i.e. the session should generate the first project in both places
        """
        response = self.client.get(reverse('setup_screen:add_project'))
        self.assertEqual(response.status_code, 302)  # assert redirecting
        response = self.client.get(reverse('setup_screen:index'))

        # assert 2 projects are expecting inputs
        self.assertContains(response, f'project-name{1}')
        self.assertContains(response, f'project-desc{1}')
        self.assertContains(response, f'project-name{2}')
        self.assertContains(response, f'project-desc{2}')
        self.assertNotContains(response, f'project-name{3}')
        self.assertNotContains(response, f'project-desc{3}')

    def test_cant_remove_single_project(self):
        """
        Ensure that the user cannot remove the last project in the list
        """
        response = self.client.get(reverse('setup_screen:remove_project', kwargs={"proj_id": 1}))
        self.assertEqual(response.status_code, 302)  # assert redirecting
        response = self.client.get(reverse('setup_screen:index'))

        # assert 1 project expecting inputs
        self.assertContains(response, f'project-name{1}')
        self.assertContains(response, f'project-desc{1}')
        self.assertNotContains(response, f'project-name{2}')
        self.assertNotContains(response, f'project-desc{2}')

    def test_add_then_remove_projects(self):
        """
        Ensure that the add and remove project endpoints both work as expected.
        Test by adding 10 projects, then removing them... ensuring all the expected ones are in the resulting html
        """
        max = 10

        # add projects
        for i in range(2, max):
            response = self.client.get(reverse('setup_screen:add_project'))

            self.assertEqual(response.status_code, 302)  # assert redirecting
            response = self.client.get(reverse('setup_screen:index'))

            # first i project inputs are present
            for j in range(1, i + 1):
                self.assertContains(response, f'project-name{j}')
                self.assertContains(response, f'project-desc{j}')

            # remaining project inputs (i+1 through max) are NOT present
            for j in range(i + 1, max + 1):
                self.assertNotContains(response, f'project-name{j}')
                self.assertNotContains(response, f'project-desc{j}')

        # remove projects (iterate in reverse)
        for i in range(max, 1, -1):
            response = self.client.get(reverse('setup_screen:remove_project', kwargs={'proj_id': 1}))

            self.assertEqual(response.status_code, 302)  # assert redirecting
            response = self.client.get(reverse('setup_screen:index'))

            # first i-1 project inputs are present
            for j in range(1, i-1):
                self.assertContains(response, f'project-name{j}')
                self.assertContains(response, f'project-desc{j}')

            # remaining project inputs (i through max) are NOT present
            for j in range(i, max+1):
                self.assertNotContains(response, f'project-name{j}')
                self.assertNotContains(response, f'project-desc{j}')

        # assert 1 project expecting inputs
        response = self.client.get(reverse('setup_screen:index'))
        self.assertContains(response, f'project-name{1}')
        self.assertContains(response, f'project-desc{1}')
        self.assertNotContains(response, f'project-name{2}')
        self.assertNotContains(response, f'project-desc{2}')

# TODO: [SetupScreen] Test that the remove button removes the inputs for the target project