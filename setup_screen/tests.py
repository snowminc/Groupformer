from django.test import TestCase, LiveServerTestCase
from django.urls import reverse

from time import sleep

from dbtools.models import *

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


class SetupScreenIntegrationTests(LiveServerTestCase):
    """
    NOTE for running tests:

    You need to download the selenium webdriver and put it in your PATH variable. See README for further details.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.driver.get(self.live_server_url + reverse('setup_screen:logout_endpoint'))

    def try_create_account(self):
        self.driver.get(self.live_server_url + reverse('setup_screen:create_account_screen'))

        self.driver.find_element_by_id('first_name').send_keys('Morgan')
        self.driver.find_element_by_id('last_name').send_keys('Freeman')
        self.driver.find_element_by_id('username').send_keys('mfreeman')
        self.driver.find_element_by_id('email').send_keys('morgan@freeman.com')
        self.driver.find_element_by_id('password').send_keys('pass1234567')
        self.driver.find_element_by_id('confirm_password').send_keys('pass1234567')

        self.driver.find_element_by_id('login-submit').click()

    def sign_in(self):
        self.driver.get(self.live_server_url + reverse('setup_screen:login_screen'))

        if 'login_screen' in self.driver.current_url:
            self.driver.find_element_by_id('username').send_keys('mfreeman')
            self.driver.find_element_by_id('password').send_keys('pass1234567')

            self.driver.find_element_by_id('login-submit').click()

    def goto_index(self, login=True):
        """
        Helper function to go to the index page
        """
        if login:
            self.try_create_account()
            self.sign_in()

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
        self.goto_index(login=False)

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

        # ensure element located on screen before proceeding
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

    def fill_complete_form_helper_method(self):
        """
        Helper method for navigating filling out the entire setup_screen form with:
        - Instructor / Groupformer info
        - roster
        - two projects
        - two attributes
        :return:
        """
        self.goto_index()

        instructor_name = "Ben Johnson"
        instructor_email = "benj1@umbc.edu"
        custom_name = "CMSC 447 Section 3"
        people_per_group = "5"
        roster_input = "Min Chon,minc1@umbc.edu\n" \
                       "Kristian Mischke,mischke1@umbc.edu\n" \
                       "Kyle Morgan,gs49698@umbc.edu\n" \
                       "Sarah Nakhon,snakhon1@umbc.edu\n" \
                       "Morgan Vanderhei,morganv2@umbc.edu\n"

        self.driver.find_element_by_id(f'instructor-name').send_keys(instructor_name)
        self.driver.find_element_by_id(f'instructor-email').send_keys(instructor_email)
        self.driver.find_element_by_id(f'custom-name').send_keys(custom_name)
        self.driver.find_element_by_id(f'people-per-group').send_keys(people_per_group)
        self.driver.find_element_by_id(f'roster-input').send_keys(roster_input)

        # add an attribute and a project for a total of 2 each
        self.click_add_attribute()
        self.click_add_project()

        # ensure contents generated before proceeding
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#project-1 .close')))

        project_0_name = "Group forming tool"
        project_0_desc = "A tool to form 447 groups that isn't a lousy Google Form. Users will be able to form groups based on project interest, team role, skill set, etc. CEO: Ben Johnson"
        project_1_name = "Open Piazza"
        project_1_desc = "An app that provides similar functionality to Piazza, but can be more greatly customized and individually managed. CEO: Frank Ferraro (Assistant Professor)"

        # assign data to the project inputs
        self.driver.find_element_by_id(f'project-name0').send_keys(project_0_name)
        self.driver.find_element_by_id(f'project-desc0').send_keys(project_0_desc)
        self.driver.find_element_by_id(f'project-name1').send_keys(project_1_name)
        self.driver.find_element_by_id(f'project-desc1').send_keys(project_1_desc)

        self.driver.find_element_by_id(f'project-desc1').send_keys(Keys.TAB)  # TAB to commit that last input

        attribute_0_name = "Do you like to punish people with puns?"
        attribute_0_homogenous = True
        attribute_1_name = "How familiar are you with Front-End development?"
        attribute_1_homogenous = False

        # assign data to the attribute inputs
        self.driver.find_element_by_id(f'attribute-name0').send_keys(attribute_0_name)
        if attribute_0_homogenous:
            self.driver.find_element_by_id(f'attribute-homogenous0').click()
        self.driver.find_element_by_id(f'attribute-name1').send_keys(attribute_1_name)
        if attribute_1_homogenous:
            self.driver.find_element_by_id(f'attribute-homogenous1').click()

        self.driver.find_element_by_id(f'attribute-homogenous1').send_keys(Keys.TAB)  # TAB to commit that last input

    def check_nothing_in_databse_helper(self):
        self.assertEqual(0, len(GroupFormer.objects.all()))
        self.assertEqual(0, len(Project.objects.all()))
        self.assertEqual(0, len(Attribute.objects.all()))
        self.assertEqual(0, len(Participant.objects.all()))
        self.assertEqual(0, len(attribute_selection.objects.all()))
        self.assertEqual(0, len(project_selection.objects.all()))

    def test_empty_input_invalid_message(self):
        """
        Test that nothing is entered in the database when a field is left blank
        Also test that invalid message is not hidden in the view
        :return:
        """
        # check nothing in DB & fill the form
        self.check_nothing_in_databse_helper()
        self.fill_complete_form_helper_method()

        # clear an input in the form
        self.driver.find_element_by_id(f'project-desc0').clear()
        self.assertEqual("", self.driver.find_element_by_id(f'project-desc0').get_attribute("value"))

        # check error not displayed
        self.assertFalse(self.driver.find_element_by_id('project-desc0-error').is_displayed())

        # submit form
        self.driver.find_element_by_id('submit-btn').click()

        sleep(1)

        # ensure contents generated before proceeding
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#project-desc0-error')))
        self.assertTrue(self.driver.find_element_by_id('project-desc0-error').is_displayed())  # error displayed

        # submit shouldn't have gone through, so nothing should remain in DB
        self.check_nothing_in_databse_helper()

    def test_invalid_email_format_instructor(self):
        """
        Test that nothing is entered in the database when the instructor email field is invalid
        Also test that invalid message is not hidden in the view
        :return:
        """
        # check nothing in DB & fill the form
        self.check_nothing_in_databse_helper()
        self.fill_complete_form_helper_method()

        # set instructor email to invalid
        instructor_email_input = self.driver.find_element_by_id(f'instructor-email')
        instructor_email_input.clear()
        instructor_email_input.send_keys("invalidemail")
        self.assertEqual("invalidemail", instructor_email_input.get_attribute("value"))

        # check error not displayed
        self.assertFalse(self.driver.find_element_by_id('instructor-email-error').is_displayed())

        # submit form
        self.driver.find_element_by_id('submit-btn').click()

        sleep(1)

        # ensure contents generated before proceeding
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#instructor-email-error')))
        self.assertTrue(self.driver.find_element_by_id('instructor-email-error').is_displayed())  # error displayed
        self.assertTrue("Invalid email address" in self.driver.find_element_by_id('instructor-email-error').get_attribute("innerHTML"))

        # submit shouldn't have gone through, so nothing should remain in DB
        self.check_nothing_in_databse_helper()

    def test_empty_roster(self):
        """
        Test that nothing is entered in the database when the roster column input is invalid
        Also test for invalid message for roster input validation
        :return:
        """
        # check nothing in DB & fill the form
        self.check_nothing_in_databse_helper()
        self.fill_complete_form_helper_method()

        # set roster to empty
        roster_input = self.driver.find_element_by_id(f'roster-input')
        roster_input.clear()
        self.assertEqual("", roster_input.get_attribute("value"))

        # check error not displayed
        self.assertFalse(self.driver.find_element_by_id('roster-input-error').is_displayed())

        # submit form
        self.driver.find_element_by_id('submit-btn').click()

        sleep(1)

        # ensure contents generated before proceeding
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#roster-input-error')))
        self.assertTrue(self.driver.find_element_by_id('roster-input-error').is_displayed())  # error displayed
        self.assertTrue("Please enter a roster of participants" in self.driver.find_element_by_id('roster-input-error').get_attribute("innerHTML"))

        # submit shouldn't have gone through, so nothing should remain in DB
        self.check_nothing_in_databse_helper()

    def test_too_few_columns_roster(self):
        """
        Test that nothing is entered in the database when the roster column input is invalid
        Also test for invalid message for roster input validation
        :return:
        """
        # check nothing in DB & fill the form
        self.check_nothing_in_databse_helper()
        self.fill_complete_form_helper_method()

        # set one participant to invalid
        roster_input = self.driver.find_element_by_id(f'roster-input')
        roster_input.clear()
        roster_input.send_keys("Person One,person1@gmail.com\nuh oh\nPerson Two,person2@gmail.com")
        self.assertEqual("Person One,person1@gmail.com\nuh oh\nPerson Two,person2@gmail.com", roster_input.get_attribute("value"))

        # check error not displayed
        self.assertFalse(self.driver.find_element_by_id('roster-input-error').is_displayed())

        # submit form
        self.driver.find_element_by_id('submit-btn').click()

        sleep(1)

        # ensure contents generated before proceeding
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#roster-input-error')))
        self.assertTrue(self.driver.find_element_by_id('roster-input-error').is_displayed())  # error displayed
        self.assertTrue("Row 2 has wrong number of columns (found 1, expected 2)" in self.driver.find_element_by_id('roster-input-error').get_attribute("innerHTML"))

        # submit shouldn't have gone through, so nothing should remain in DB
        self.check_nothing_in_databse_helper()

    def test_too_many_columns_roster(self):
        """
        Test that nothing is entered in the database when the roster column input is invalid
        Also test for invalid message for roster input validation
        :return:
        """
        # check nothing in DB & fill the form
        self.check_nothing_in_databse_helper()
        self.fill_complete_form_helper_method()

        # set one participant to invalid
        roster_input = self.driver.find_element_by_id(f'roster-input')
        roster_input.clear()
        roster_input.send_keys("Person One,person1@gmail.com\nPerson Two,person2@gmail.com,oops too many columns")
        self.assertEqual("Person One,person1@gmail.com\nPerson Two,person2@gmail.com,oops too many columns", roster_input.get_attribute("value"))

        # check error not displayed
        self.assertFalse(self.driver.find_element_by_id('roster-input-error').is_displayed())

        # submit form
        self.driver.find_element_by_id('submit-btn').click()

        sleep(1)

        # ensure contents generated before proceeding
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#roster-input-error')))
        self.assertTrue(self.driver.find_element_by_id('roster-input-error').is_displayed())  # error displayed
        self.assertTrue("Row 2 has wrong number of columns (found 3, expected 2)" in self.driver.find_element_by_id(
            'roster-input-error').get_attribute("innerHTML"))

        # submit shouldn't have gone through, so nothing should remain in DB
        self.check_nothing_in_databse_helper()

    def test_invalid_email_format_roster(self):
        """
        Test that nothing is entered in the database when the roster email input is invalid
        Also test for invalid message for roster input validation
        :return:
        """
        # check nothing in DB & fill the form
        self.check_nothing_in_databse_helper()
        self.fill_complete_form_helper_method()

        # set one participant to invalid
        roster_input = self.driver.find_element_by_id(f'roster-input')
        roster_input.clear()
        roster_input.send_keys("Person One,person1@gmail.com\nPerson Two,person2.com")
        self.assertEqual("Person One,person1@gmail.com\nPerson Two,person2.com",
                         roster_input.get_attribute("value"))

        # check error not displayed
        self.assertFalse(self.driver.find_element_by_id('roster-input-error').is_displayed())

        # submit form
        self.driver.find_element_by_id('submit-btn').click()

        sleep(1)

        # ensure contents generated before proceeding
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#roster-input-error')))
        self.assertTrue(self.driver.find_element_by_id('roster-input-error').is_displayed())  # error displayed
        self.assertTrue("Row 2 contains invalid email address" in self.driver.find_element_by_id(
            'roster-input-error').get_attribute("innerHTML"))

        # submit shouldn't have gone through, so nothing should remain in DB
        self.check_nothing_in_databse_helper()

    def test_empty_name_roster(self):
        """
        Test that nothing is entered in the database when the roster email input is invalid
        Also test for invalid message for roster input validation
        :return:
        """
        # check nothing in DB & fill the form
        self.check_nothing_in_databse_helper()
        self.fill_complete_form_helper_method()

        # set one participant to invalid
        roster_input = self.driver.find_element_by_id(f'roster-input')
        roster_input.clear()
        roster_input.send_keys("Person One,person1@gmail.com\n,person@gmail.com")
        self.assertEqual("Person One,person1@gmail.com\n,person@gmail.com", roster_input.get_attribute("value"))

        # check error not displayed
        self.assertFalse(self.driver.find_element_by_id('roster-input-error').is_displayed())

        # submit form
        self.driver.find_element_by_id('submit-btn').click()

        sleep(1)

        # ensure contents generated before proceeding
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'#roster-input-error')))
        self.assertTrue(self.driver.find_element_by_id('roster-input-error').is_displayed())  # error displayed
        self.assertTrue("Row 2 contains has empty name" in self.driver.find_element_by_id(
            'roster-input-error').get_attribute("innerHTML"))

        # submit shouldn't have gone through, so nothing should remain in DB
        self.check_nothing_in_databse_helper()

    def test_fill_and_submit_form_to_database(self):
        """
        Integration test that fills out the entire form and submits it to the backend
        """
        # check empty database and fill the form
        self.check_nothing_in_databse_helper()
        self.fill_complete_form_helper_method()

        # submit form
        self.driver.find_element_by_id('submit-btn').click()

        # click OK on the alert that pops up. NOTE: in the future we will probably remove this default alert
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

        # simple: assert by counting
        self.assertEqual(1, len(GroupFormer.objects.all()))
        self.assertEqual(2, len(Project.objects.all()))
        self.assertEqual(2, len(Attribute.objects.all()))
        self.assertEqual(5, len(Participant.objects.all()))
        self.assertEqual(0, len(attribute_selection.objects.all()))
        self.assertEqual(0, len(project_selection.objects.all()))

        # ensure groupformer was properly added
        gf = GroupFormer.objects.all()[0]
        self.assertEqual("Ben Johnson", gf.prof_name)
        self.assertEqual("benj1@umbc.edu", gf.prof_email)
        self.assertEqual("CMSC 447 Section 3", gf.class_section)
        # TODO: self.assertEqual(5, gf.people_per_group)

        # ensure participants were properly added to the groupformer
        part_min = gf.getParticipantByEmail("minc1@umbc.edu")
        self.assertIsNotNone(part_min)
        self.assertEqual("Min Chon", part_min.part_name)

        part_kristian = gf.getParticipantByEmail("mischke1@umbc.edu")
        self.assertIsNotNone(part_kristian)
        self.assertEqual("Kristian Mischke", part_kristian.part_name)

        part_klye = gf.getParticipantByEmail("gs49698@umbc.edu")
        self.assertIsNotNone(part_klye)
        self.assertEqual("Kyle Morgan", part_klye.part_name)

        part_sarah = gf.getParticipantByEmail("snakhon1@umbc.edu")
        self.assertIsNotNone(part_sarah)
        self.assertEqual("Sarah Nakhon", part_sarah.part_name)

        part_morgan = gf.getParticipantByEmail("morganv2@umbc.edu")
        self.assertIsNotNone(part_morgan)
        self.assertEqual("Morgan Vanderhei", part_morgan.part_name)

        # ensure projects are properly added to groupformer
        proj_group = gf.getProject("Group forming tool")
        self.assertIsNotNone(proj_group)
        self.assertEqual("A tool to form 447 groups that isn't a lousy Google Form. Users will be able to form groups based on project interest, team role, skill set, etc. CEO: Ben Johnson", proj_group.project_description)

        proj_piazza = gf.getProject("Open Piazza")
        self.assertIsNotNone(proj_piazza)
        self.assertEqual("An app that provides similar functionality to Piazza, but can be more greatly customized and individually managed. CEO: Frank Ferraro (Assistant Professor)", proj_piazza.project_description)

        # ensure attributes are properly added to groupformer
        attr_puns = gf.getAttribute("Do you like to punish people with puns?")
        self.assertIsNotNone(attr_puns)
        self.assertTrue(attr_puns.is_homogenous)

        attr_front_end = gf.getAttribute("How familiar are you with Front-End development?")
        self.assertIsNotNone(attr_front_end)
        self.assertFalse(attr_front_end.is_homogenous)

class LoginTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.driver.get(self.live_server_url + reverse('setup_screen:logout_endpoint'))

    def try_create_account(self):
        self.driver.get(self.live_server_url + reverse('setup_screen:create_account_screen'))

        self.driver.find_element_by_id('first_name').send_keys('Morgan')
        self.driver.find_element_by_id('last_name').send_keys('Freeman')
        self.driver.find_element_by_id('username').send_keys('mfreeman')
        self.driver.find_element_by_id('email').send_keys('morgan@freeman.com')
        self.driver.find_element_by_id('password').send_keys('pass1234567')
        self.driver.find_element_by_id('confirm_password').send_keys('pass1234567')

        self.driver.find_element_by_id('login-submit').click()

    def sign_in(self, username, password, redirect=""):
        self.driver.get(self.live_server_url + reverse('setup_screen:login_screen') + f'?redirect={redirect}')

        if 'login_screen' in self.driver.current_url:
            self.driver.find_element_by_id('username').send_keys(username)
            self.driver.find_element_by_id('password').send_keys(password)

            self.driver.find_element_by_id('login-submit').click()

    def goto_index(self, login=True):
        """
        Helper function to go to the index page
        """
        if login:
            self.try_create_account()
            self.sign_in('mfreeman', 'pass1234567')

        self.driver.get(self.live_server_url + reverse('setup_screen:index'))

    def test_no_account(self):
        """
            Test error when using incorrect username
        """

        self.sign_in('no_account', 'oh_no_thats_no_good')

        self.assertEqual('Could not authenticate user', self.driver.find_element_by_id('error-message').text)

    def test_setup_then_redirect(self):
        """
            Test redirecting to response screen from login page after already signed in
        """

        # create account and sign in
        self.goto_index()

        # navigate to login screen should auto-redirect to setup index because we're logged in already
        self.driver.get(self.live_server_url + reverse('setup_screen:login_screen'))
        self.assertTrue(self.driver.current_url.endswith('setup_screen/'))

        # navigate to login screen with redirect=results_screen, should auto-redirect there because already logged in
        self.driver.get(self.live_server_url + reverse('setup_screen:login_screen') + "?redirect=results_screen")
        self.assertTrue(self.driver.current_url.endswith('results_screen/'))

    def test_setup_then_redirect_logged_out(self):
        """
            Test redirecting to response screen from login page after account is created, but logged out
        """

        # create account and sign in
        self.goto_index()

        # logout and login with redirect to results_screen
        self.driver.find_element_by_id('logout-btn').click()
        self.sign_in('mfreeman', 'pass1234567', 'results_screen')
        self.assertTrue(self.driver.current_url.endswith('results_screen/'))

        # logout and login without redirect
        self.driver.find_element_by_id('logout-btn').click()
        self.sign_in('mfreeman', 'pass1234567')
        self.assertTrue(self.driver.current_url.endswith('setup_screen/'))

    def test_create_account_pass_too_short(self):
        """
            Test that creating an account with short password fails
        """

        self.driver.get(self.live_server_url + reverse('setup_screen:create_account_screen'))

        self.driver.find_element_by_id('first_name').send_keys('Morgan')
        self.driver.find_element_by_id('last_name').send_keys('Freeman')
        self.driver.find_element_by_id('username').send_keys('mfreeman')
        self.driver.find_element_by_id('email').send_keys('morgan@freeman.com')
        self.driver.find_element_by_id('password').send_keys('xx')
        self.driver.find_element_by_id('confirm_password').send_keys('xx')

        self.driver.find_element_by_id('login-submit').click()
        self.assertEqual('Password must be 6 or more characters!', self.driver.find_element_by_id('error-message').text)

    def test_create_account_pass_dont_match(self):
        """
            Test that creating an account with mismatch confirmed password fails
        """

        self.driver.get(self.live_server_url + reverse('setup_screen:create_account_screen'))

        self.driver.find_element_by_id('first_name').send_keys('Morgan')
        self.driver.find_element_by_id('last_name').send_keys('Freeman')
        self.driver.find_element_by_id('username').send_keys('mfreeman')
        self.driver.find_element_by_id('email').send_keys('morgan@freeman.com')
        self.driver.find_element_by_id('password').send_keys('helloDarknessMyOldFriend')
        self.driver.find_element_by_id('confirm_password').send_keys('password1234567')

        self.driver.find_element_by_id('login-submit').click()
        self.assertEqual('Passwords do not match!', self.driver.find_element_by_id('error-message').text)

    def test_create_account_username_taken(self):
        """
            Test that creating an account with an existing username fails
        """
        self.try_create_account()

        self.driver.get(self.live_server_url + reverse('setup_screen:create_account_screen'))

        self.driver.find_element_by_id('first_name').send_keys('Morgan')
        self.driver.find_element_by_id('last_name').send_keys('Freeman')
        self.driver.find_element_by_id('username').send_keys('mfreeman')
        self.driver.find_element_by_id('email').send_keys('morgan@freeman123.com')
        self.driver.find_element_by_id('password').send_keys('helloDarknessMyOldFriend')
        self.driver.find_element_by_id('confirm_password').send_keys('helloDarknessMyOldFriend')

        self.driver.find_element_by_id('login-submit').click()
        self.assertEqual('Username already taken!', self.driver.find_element_by_id('error-message').text)

    def test_create_account_email_taken(self):
        """
            Test that creating an account with existing email fails
        """
        self.try_create_account()

        self.driver.get(self.live_server_url + reverse('setup_screen:create_account_screen'))

        self.driver.find_element_by_id('first_name').send_keys('Morgan')
        self.driver.find_element_by_id('last_name').send_keys('Freeman')
        self.driver.find_element_by_id('username').send_keys('mfreeman2')
        self.driver.find_element_by_id('email').send_keys('morgan@freeman.com')
        self.driver.find_element_by_id('password').send_keys('helloDarknessMyOldFriend')
        self.driver.find_element_by_id('confirm_password').send_keys('helloDarknessMyOldFriend')

        self.driver.find_element_by_id('login-submit').click()
        self.assertEqual('Email already taken!', self.driver.find_element_by_id('error-message').text)
