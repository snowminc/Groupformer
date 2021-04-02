from django.test import TestCase, LiveServerTestCase
from django.urls import reverse

import time

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

    Further Note: Currently an issue with Chrome v89 that will be fixed in v90 but is currently in beta.
    Selenium will spew some warning messages, but this doesn't effect the integration tests aside from
    clogging the terminal output.
    - https://stackoverflow.com/questions/65080685/usb-usb-device-handle-win-cc1020-failed-to-read-descriptor-from-node-connectio
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

    def click_remove_project(self, index: int):
        """
        Helper function to click the remove project button of given index
        :param index:index of the project to remove
        """
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#project-{index} .close')))
        self.driver.execute_script(f'$("#project-{index} .close").click()')

    def click_add_attribute(self):
        """
        Helper function to click the add attribute button
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'add-attribute-btn'))).click()

    def click_remove_attribute(self, index: int):
        """
        Helper function to click the remove attribute button
        :param index:index of the attribute to remove
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#attribute-{index} .close')))
        self.driver.execute_script(f'$("#attribute-{index} .close").click()')

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

    def test_remove_correct_project_indices(self):
        """
        Ensure that the remove project button removes the correct project indices
        """
        self.goto_index()

        # add two projects for a total of 3
        self.click_add_project()
        self.click_add_project()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#project-2 .close')))

        project_0_name = "Project 0 - Jules has Hope"
        project_0_desc = "In a Cat Galaxy far far away..."
        project_1_name = "Project 1 - He Claws Back"
        project_1_desc = "Dun Dun Dunnnn"
        project_2_name = "Project 2 - Return of the Jules"
        project_2_desc = "Victory!"

        # assign data to the inputs
        self.driver.find_element_by_id(f'project-name0').send_keys(project_0_name)
        self.driver.find_element_by_id(f'project-desc0').send_keys(project_0_desc)
        self.driver.find_element_by_id(f'project-name1').send_keys(project_1_name)
        self.driver.find_element_by_id(f'project-desc1').send_keys(project_1_desc)
        self.driver.find_element_by_id(f'project-name2').send_keys(project_2_name)
        self.driver.find_element_by_id(f'project-desc2').send_keys(project_2_desc)

        self.driver.find_element_by_id(f'project-desc2').send_keys(Keys.TAB)  # TAB to commit that last input

        self.click_remove_project(0)

        # check that indices 0 and 1 correspond to the prior 1 and 2
        self.assertEqual(project_1_name, self.driver.find_element_by_id(f'project-name0').get_attribute("value"))
        self.assertEqual(project_1_desc, self.driver.find_element_by_id(f'project-desc0').get_attribute("value"))
        self.assertEqual(project_2_name, self.driver.find_element_by_id(f'project-name1').get_attribute("value"))
        self.assertEqual(project_2_desc, self.driver.find_element_by_id(f'project-desc1').get_attribute("value"))

        self.click_remove_project(0)

        # check that index 0 is the original index 2
        self.assertEqual(project_2_desc, self.driver.find_element_by_id(f'project-desc0').get_attribute("value"))
        self.assertEqual(project_2_name, self.driver.find_element_by_id(f'project-name0').get_attribute("value"))

    def test_attributes_cumulative(self):
        """
        Test similar to the project tests that combines more than one together and tests:
        - Adding
        - Removing
        - Removing when 1 left
        """
        self.goto_index()

        # add two attributes for a total of 3
        self.click_add_attribute()
        self.click_add_attribute()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#attribute-2 .close')))

        # ensure the added attributes are present (indices 0-2)
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-name0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-homogenous0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-name1'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-homogenous1'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-name2'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-homogenous2'))
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'attribute-name3')
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'attribute-homogenous3')

        attribute_0_name = "Do you like memes?"
        attribute_0_homogenous = True
        attribute_1_name = "Rate your slug farming skills"
        attribute_1_homogenous = False
        attribute_2_name = "Would you rather pick a high or a low number?"
        attribute_2_homogenous = True

        # assign data to the inputs
        self.driver.find_element_by_id(f'attribute-name0').send_keys(attribute_0_name)
        if attribute_0_homogenous:
            self.driver.find_element_by_id(f'attribute-homogenous0').click()
        self.driver.find_element_by_id(f'attribute-name1').send_keys(attribute_1_name)
        if attribute_1_homogenous:
            self.driver.find_element_by_id(f'attribute-homogenous1').click()
        self.driver.find_element_by_id(f'attribute-name2').send_keys(attribute_2_name)
        if attribute_2_homogenous:
            self.driver.find_element_by_id(f'attribute-homogenous2').click()

        self.driver.find_element_by_id(f'attribute-homogenous2').send_keys(Keys.TAB)  # TAB to commit that last input

        self.click_remove_attribute(0) # remove index 0

        # check that indices 0 & 1 exist, and index 2 does not
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-name0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-homogenous0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-name1'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-homogenous1'))
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'attribute-name2')
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'attribute-homogenous2')

        # check that indices 0 and 1 correspond to the prior 1 and 2 values
        self.assertEqual(attribute_1_name, self.driver.find_element_by_id(f'attribute-name0').get_attribute("value"))
        self.assertEqual(attribute_1_homogenous, self.driver.find_element_by_id(f'attribute-homogenous0').is_selected())
        self.assertEqual(attribute_2_name, self.driver.find_element_by_id(f'attribute-name1').get_attribute("value"))
        self.assertEqual(attribute_2_homogenous, self.driver.find_element_by_id(f'attribute-homogenous1').is_selected())

        self.click_remove_attribute(0)

        # check that ONLY index 0 remains
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-name0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-homogenous0'))
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'attribute-name1')
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'attribute-homogenous1')

        # check that index 0 is the original index 2
        self.assertEqual(attribute_2_homogenous, self.driver.find_element_by_id(f'attribute-homogenous0').is_selected())
        self.assertEqual(attribute_2_name, self.driver.find_element_by_id(f'attribute-name0').get_attribute("value"))

        # try remove when only one item left
        self.click_remove_attribute(0)

        # same element 0 remains
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-name0'))
        self.assertIsNotNone(self.driver.find_element_by_id(f'attribute-homogenous0'))
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'attribute-name1')
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, f'attribute-homogenous1')

        # check that index 0 is the original index 2
        self.assertEqual(attribute_2_homogenous, self.driver.find_element_by_id(f'attribute-homogenous0').is_selected())
        self.assertEqual(attribute_2_name, self.driver.find_element_by_id(f'attribute-name0').get_attribute("value"))

# TODO: Integration test that fills out the project/attribute fields, then submits and checks the database for the changes