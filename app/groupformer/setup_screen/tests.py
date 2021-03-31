from django.test import TestCase, LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


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
        #response = self.client.get(reverse('setup_screen:index'))
        #self.assertContains(response, 'project-name1')
        pass


class SetupScreenIntegrationTests(LiveServerTestCase):
    """
    NOTE for running tests:

    You need to download the selenium webdriver and put it in your PATH variable.

    - Download: https://chromedriver.chromium.org/downloads
    - Make sure this matches your chrome version
    - Update PATH Environment Variable:
    - Windows:
        - Save `chromedriver.exe` to a path such as `C:\Program Files\Selenium`
        - Press the windows button and search 'advanced system settings'
        - Click 'Environment Variables'
        - Edit your User or System `PATH` variable adding the directory you chose
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def goto_index(self):
        """
        Helper function to go to the index page
        """
        self.driver.get(self.live_server_url + reverse('setup_screen:index'))

    def click_add_project(self):
        """
        Helper function to click the add project button
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'add-project-btn'))).click()

    def click_remove_project(self, index):
        """
        Helper function to click the remove project button
        """
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#project-{index} .close')))
        self.driver.execute_script(f'$("#project-{index} .close").click()')

    def test_single_project_inputs_exist(self):
        """
        Ensure that only a single project input exists when first loading the setup screen page
        """
        self.goto_index()
        self.assertTrue("GroupFormer" in self.driver.title)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'add-project-btn')))

        self.assertIsNotNone(self.driver.find_element_by_id("project-name0"))
        self.assertIsNotNone(self.driver.find_element_by_id("project-desc0"))
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, "project-name1")
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, "project-desc1")

    def test_add_projects_reset_after_load(self):
        """
        Current functionality expects that the form resets when the page is loaded, this may change with a stretch goal
        """
        self.goto_index()

        # add one additional project
        self.click_add_project()

        # ensure that 0 and 1 inputs exist
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-name0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-desc0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-name1'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-desc1'))
        # ensure input 2 does NOT exist
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-name2')
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-desc2')

        # reload page
        self.goto_index()

        # only project input 0 should exist
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-name0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-desc0'))
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-name1')
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-desc1')

    def test_add_projects_inputs_exist(self):
        """
        Ensure that the add project button adds a new project to be displayed on the setup screen
        """
        self.goto_index()

        for i in range(1, 10):
            self.click_add_project()

            # ensure that the existing 0 through i+1 inputs exist
            for j in range(0, i+1):
                self.assertIsNotNone(self.driver.find_element_by_id(f'project-name{j}'))
                self.assertIsNotNone(self.driver.find_element_by_id(f'project-desc{j}'))

            # ensure the i+2 input does NOT exist
            self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-name{i+2}')
            self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-desc{i + 2}')

    def test_cant_remove_single_project(self):
        """
        Ensure that the user cannot remove the last project in the list
        """
        self.goto_index()

        # click button to remove project 0
        self.click_remove_project(0)

        # assert project 0 expecting inputs
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-name0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-desc0'))
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-name1')
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-desc1')

    def test_add_then_remove_projects(self):
        """
        Ensure that the add and remove project endpoints both work as expected.
        Test by adding 10 projects, then removing them... ensuring all the expected ones are in the resulting html
        """
        self.goto_index()
        max = 10

        # add projects
        for i in range(1, max):
            self.click_add_project()

            # first i project inputs are present
            for j in range(0, i + 1):
                self.assertIsNotNone(self.driver.find_element_by_id(f'project-name{j}'))
                self.assertIsNotNone(self.driver.find_element_by_id(f'project-desc{j}'))

            # remaining project inputs (i+1 through max) are NOT present
            for j in range(i + 1, max + 1):
                self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-name{j}')
                self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-desc{j}')

        # remove projects (iterate in reverse so that it's easier to loop to the last expected element)
        for i in range(max, 1, -1):
            self.click_remove_project(0)  # remove 0th project

            # first i-1 project inputs are present
            for j in range(0, i - 1):
                self.assertIsNotNone(self.driver.find_element_by_id(f'project-name{j}'))
                self.assertIsNotNone(self.driver.find_element_by_id(f'project-desc{j}'))

            # remaining project inputs (i through max) are NOT present
            for j in range(i, max + 1):
                self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-name{j}')
                self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-desc{j}')

        # assert ONLY project 0 expecting inputs
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-name0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'project-desc0'))
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-desc1')
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'project-name1')

# TODO: [SetupScreen] Test that the remove button removes the inputs for the target project