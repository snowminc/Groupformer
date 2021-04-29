from django.test import TestCase
from django.urls import reverse

from dbtools.models import *


def create_sample_groupformer():
    gfs = {}
    gfs[1] = {}
    gfs[1]['gf'] = GroupFormer.objects.create(prof_name="Min Chon", prof_email="minc1@umbc.edu", class_section="34")
    gfs[2] = {}
    gfs[2]['gf'] = GroupFormer.objects.create(prof_name="Ben Johnson", prof_email="ben.johnson@umbc.edu", class_section="24")
    return gfs

def create_sample_projects(gfs):
    gfs[1]['p1'] = Project.objects.create(group_former=gfs[1]['gf'], project_name="Groupformer Tool", project_description="Create a tool that creates groups!")
    gfs[1]['p2'] = Project.objects.create(group_former=gfs[1]['gf'], project_name="Robot that pees beer", project_description="Create a modification on a very expensive robot dog!")
    
    gfs[2]['p1'] = Project.objects.create(group_former=gfs[2]['gf'], project_name="Literally Something", project_description="Literally Anything!")
    gfs[2]['p2'] = Project.objects.create(group_former=gfs[2]['gf'], project_name="What", project_description="I dont know.")


def create_sample_attributes(gfs):
    # Intentionally do not create attributes for second groupformer
    gfs[1]['a1'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Back-End", is_homogenous=False, is_continuous=True)
    gfs[1]['a2'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Front-End", is_homogenous=True, is_continuous=True)
    gfs[1]['a3'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Dog Lover", is_homogenous=False, is_continuous=False)


def create_sample_participants(gfs):
    names = ["Min","Kristian","Sarah","Morgan","Kyle","Ben","Eric","Andrew"]
    for i in range(len(names)):
        gfs[1]['part'+str(i+1)] = Participant.objects.create(group_former=gfs[1]['gf'], part_name=names[i], part_email="example@email.com")
        gfs[2]['part'+str(i+1)] = Participant.objects.create(group_former=gfs[2]['gf'], part_name=names[i], part_email="example@email.com")
    return names


def create_all_samples():
    gfs = create_sample_groupformer()
    create_sample_projects(gfs)
    create_sample_attributes(gfs)
    create_sample_participants(gfs)
    return gfs


class MinIteration3ResponseScreenTests(TestCase):
    def test_displays_all_projects(self):
        """
        Check if the projects created appear on the form
        """
        create_all_samples()
        response = self.client.get(reverse('response_screen:response_screen', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Groupformer Tool")
        self.assertContains(response, "Robot that pees beer")
        self.assertContains(response, "Create a tool that creates groups!")
        self.assertContains(response, "Create a modification on a very expensive robot dog!")
        response = self.client.get(reverse('response_screen:response_screen', args=(2,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Literally Something")
        self.assertContains(response, "What")
        self.assertContains(response, "Literally Anything!")
        self.assertContains(response, "I dont know.")

    def test_displays_projects_without_attributes(self):
        """
        Check if the form still displays projects even if no attributes were created
        """
        gfs = create_sample_groupformer()
        create_sample_projects(gfs)
        create_sample_participants(gfs)
        response = self.client.get(reverse('response_screen:response_screen', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Groupformer Tool")
        self.assertContains(response, "Robot that pees beer")
        self.assertContains(response, "Create a tool that creates groups!")
        self.assertContains(response, "Create a modification on a very expensive robot dog!")
        response = self.client.get(reverse('response_screen:response_screen', args=(2,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Literally Something")
        self.assertContains(response, "What")
        self.assertContains(response, "Literally Anything!")
        self.assertContains(response, "I dont know.")

    def test_displays_all_attributes(self):
        """
        Check if all attributes appear on the form
        """
        create_all_samples()
        response = self.client.get(reverse('response_screen:response_screen', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Back-End")
        self.assertContains(response, "Front-End")
        self.assertContains(response, "Dog Lover")
        # The second GroupFormer intentionally does not have any attributes
        response = self.client.get(reverse('response_screen:response_screen', args=(2,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Back-End")
        self.assertNotContains(response, "Front-End")
        self.assertNotContains(response, "Dog Lover")

    def test_displays_attributes_without_projects(self):
        """
        Check if the form still displays attributes even if no projects were created
        """
        gfs = create_sample_groupformer()
        create_sample_attributes(gfs)
        create_sample_participants(gfs)
        response = self.client.get(reverse('response_screen:response_screen', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Back-End")
        self.assertContains(response, "Front-End")
        self.assertContains(response, "Dog Lover")
        # The second GroupFormer intentionally does not have any attributes
        response = self.client.get(reverse('response_screen:response_screen', args=(2,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Back-End")
        self.assertNotContains(response, "Front-End")
        self.assertNotContains(response, "Dog Lover")
    
    def test_displays_without_projects_or_attributes(self):
        """
        Check if the form still displays despite no projects and attributes created
        """
        gfs = create_sample_groupformer()
        create_sample_participants(gfs)
        response = self.client.get(reverse('response_screen:response_screen', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Name")
        self.assertContains(response, "E-mail")

    def test_displays_participants(self):
        """
        Test that the form lists EVERY participant in the preference selection box
        """
        gfs = create_sample_groupformer()
        names = create_sample_participants(gfs)
        response1 = self.client.get(reverse('response_screen:response_screen', args=(1,)))
        response2 = self.client.get(reverse('response_screen:response_screen', args=(2,)))
        for i in range(len(names)):
            self.assertContains(response1, names[i])
            self.assertContains(response2, names[i])

    

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver



class SeleniumResponseScreen(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_missing_projects_preference(self):
        """
        Test if the error message shows if user does not input a preference for a project.
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id

        # Test for the first groupformer object
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
        # Name and Email
        self.selenium.find_element_by_xpath("//input[@id='participantNameForm']").send_keys("Min Chon")
        self.selenium.find_element_by_xpath("//input[@id='participantEmailForm']").send_keys("minc1@umbc.edu")
        # Select preferences for both projects
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='Very Interested']".format(gfs[1]['p1'].pk)).click()

        # Remove the second project to test missing error
        #self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='PLEASE NO']".format(gfs[1]['p2'].pk)).click()

        # Select preferences for all attributes
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='4']".format(gfs[1]['a1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='2']".format(gfs[1]['a2'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='5 (Most preferred)']".format(gfs[1]['a3'].pk)).click()
        # Select a few students
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Kristian']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Min']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Ben']").click()
        # Submit
        self.selenium.find_element_by_xpath("//button[@id='submitForm']").click()

        error_message = self.selenium.find_element_by_xpath("//div[@id='projForm{}_error']".format(gfs[1]['p2'].pk))
        # Using .text instead of .get_attribute("innerHTML") because innerHTML still contains the error, but is hidden
        #  on display. .text only shows what the user sees (ignores any `display: hidden` text)
        self.assertTrue("Must select a preference for this project."  in error_message.text)


    def test_missing_attributes_preference(self):
        """
        Test if the error message shows if user does not input a preference for an attribute.
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id

        # Test for the first groupformer object
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
        # Name and Email
        self.selenium.find_element_by_xpath("//input[@id='participantNameForm']").send_keys("Min Chon")
        self.selenium.find_element_by_xpath("//input[@id='participantEmailForm']").send_keys("minc1@umbc.edu")
        # Select preferences for both projects
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='Very Interested']".format(gfs[1]['p1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='PLEASE NO']".format(gfs[1]['p2'].pk)).click()
        # Select preferences for all attributes
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='4']".format(gfs[1]['a1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='2']".format(gfs[1]['a2'].pk)).click()

        # Remove the third attribute to test missing error
        #self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='5 (Most preferred)']".format(gfs[1]['a3'].pk)).click()

        # Select a few students
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Kristian']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Min']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Ben']").click()
        # Submit
        self.selenium.find_element_by_xpath("//button[@id='submitForm']").click()

        error_message = self.selenium.find_element_by_xpath("//div[@id='attrForm{}_error']".format(gfs[1]['a3'].pk))
        # Using .text instead of .get_attribute("innerHTML") because innerHTML still contains the error, but is hidden
        #  on display. .text only shows what the user sees (ignores any `display: hidden` text)
        self.assertTrue("Must select a preference for this attribute." in error_message.text)


    def test_missing_user_info(self):
        """
        Test if the error message shows if user does not input a preference for an attribute.
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id

        # Test for the first groupformer object
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
        # Name and Email

        # Remove user info to test missing error
        #self.selenium.find_element_by_xpath("//input[@id='participantNameForm']").send_keys("Min Chon")
        #self.selenium.find_element_by_xpath("//input[@id='participantEmailForm']").send_keys("minc1@umbc.edu")

        # Select preferences for both projects
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='Very Interested']".format(gfs[1]['p1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='PLEASE NO']".format(gfs[1]['p2'].pk)).click()
        # Select preferences for all attributes
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='4']".format(gfs[1]['a1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='2']".format(gfs[1]['a2'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='5 (Most preferred)']".format(gfs[1]['a3'].pk)).click()
        # Select a few students
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Kristian']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Min']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Ben']").click()
        # Submit
        self.selenium.find_element_by_xpath("//button[@id='submitForm']").click()

        name_error_message = self.selenium.find_element_by_xpath("//div[@id='participantNameForm_error']")
        email_error_message = self.selenium.find_element_by_xpath("//div[@id='participantEmailForm_error']")
        # Using .text instead of .get_attribute("innerHTML") because innerHTML still contains the error, but is hidden
        #  on display. .text only shows what the user sees (ignores any `display: hidden` text)
        self.assertTrue("Must enter your name." in name_error_message.text)
        self.assertTrue("Must enter your e-mail." in email_error_message.text)


    def test_fill_response_screen(self):
        """
        Test that users are required to input important fields such as Name, Email, and all preference boxes
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id
        gfs2 = gfs[2]['gf'].id

        #########################################
        # Test for the first groupformer object #
        #########################################
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
        # Name and Email
        self.selenium.find_element_by_xpath("//input[@id='participantNameForm']").send_keys("Min Chon")
        self.selenium.find_element_by_xpath("//input[@id='participantEmailForm']").send_keys("minc1@umbc.edu")
        # Select preferences for both projects
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='Very Interested']".format(gfs[1]['p1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='PLEASE NO']".format(gfs[1]['p2'].pk)).click()
        # Select preferences for all attributes
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='4']".format(gfs[1]['a1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='2']".format(gfs[1]['a2'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='5 (Most preferred)']".format(gfs[1]['a3'].pk)).click()
        # Select a few students
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Kristian']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Min']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Ben']").click()
        # Submit
        self.selenium.find_element_by_xpath("//button[@id='submitForm']").click()

        # Currently, the form is set to post to current page, leaving parameters in the URL.
        url = self.selenium.current_url
        # Isolate the parameters of the POSTed form
        param_url = url.rsplit('?', 1)[1]
        params = param_url.split("&")
        for i in range(len(params)):
            # Replace symbol placeholders with correct character
            params[i] = params[i].replace("+", " ")
            params[i] = params[i].replace("%40", "@")
            # Create name, value pairs
            params[i] = tuple(params[i].split("="))

        # For each attribute form, the homogenous/continuous values are a hidden form retrieved from the model.
        # Check if those attributes carried over the correct values for those model objects.
        self.assertTrue(len(params)==11)  # Check that only the following 10 tuples exist (plus CSRF token)
        self.assertTrue(('participantNameForm', 'Min Chon') in params)
        self.assertTrue(('participantEmailForm', 'minc1@umbc.edu') in params)
        self.assertTrue(('projForm{}_preference'.format(gfs[1]['p1'].pk), '5') in params)
        self.assertTrue(('projForm{}_preference'.format(gfs[1]['p2'].pk), '1') in params)
        self.assertTrue(('attrForm{}_preference'.format(gfs[1]['a1'].pk), '4') in params)
        self.assertTrue(('attrForm{}_preference'.format(gfs[1]['a2'].pk), '2') in params)
        self.assertTrue(('attrForm{}_preference'.format(gfs[1]['a3'].pk), '5') in params)
        self.assertTrue(('participantForm_preference', 'Min') in params)
        self.assertTrue(('participantForm_preference', 'Kristian') in params)
        self.assertTrue(('participantForm_preference', 'Ben') in params)

        ##########################################
        # Test for the second groupformer object #
        ##########################################
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs2}))
        # Name and Email
        self.selenium.find_element_by_xpath("//input[@id='participantNameForm']").send_keys("Bobby Bobberson")
        self.selenium.find_element_by_xpath("//input[@id='participantEmailForm']").send_keys("bobbybob@umbc.edu")
        # Select preferences for both projects
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='Neutral']".format(gfs[2]['p1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='Somewhat Interested']".format(gfs[2]['p2'].pk)).click()
        # Select preferences for all attributes (None :D)
        # Select a few students
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Sarah']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Kyle']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Morgan']").click()
        # Submit
        self.selenium.find_element_by_xpath("//button[@id='submitForm']").click()

        # Currently, the form is set to post to current page, leaving parameters in the URL.
        url = self.selenium.current_url
        # Isolate the parameters of the POSTed form
        param_url = url.rsplit('?', 1)[1]
        params = param_url.split("&")
        for i in range(len(params)):
            # Replace symbol placeholders with correct character
            params[i] = params[i].replace("+", " ")
            params[i] = params[i].replace("%40", "@")
            # Create name, value pairs
            params[i] = tuple(params[i].split("="))

        # Attributes do not exist on this Groupformer instance, do not check for them
        self.assertTrue(len(params)==8)  # Check that only the following 7 tuples exist (plus CSRF token)
        self.assertTrue(('participantNameForm', 'Bobby Bobberson') in params)
        self.assertTrue(('participantEmailForm', 'bobbybob@umbc.edu') in params)
        self.assertTrue(('projForm{}_preference'.format(gfs[2]['p1'].pk), '3') in params)
        self.assertTrue(('projForm{}_preference'.format(gfs[2]['p2'].pk), '4') in params)
        self.assertTrue(('participantForm_preference', 'Sarah') in params)
        self.assertTrue(('participantForm_preference', 'Kyle') in params)
        self.assertTrue(('participantForm_preference', 'Morgan') in params)


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from dbtools.models import *


class LoginScreenTest(StaticLiveServerTestCase):
    @classmethod
    def setUp(cls):
        gf = addGroupFormer("Ben Johnson", "bjohn@umbc.edu", "CMSC 447-01")
        gf.addParticipant("John Beachy", "johnny@niu.edu")

        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(self.live_server_url + reverse('response_screen:login', kwargs={'groupformer_id': 1}))

        # No alert on first look
        with self.assertRaises(NoSuchElementException):
            alert = self.selenium.find_element_by_id('bad-email')

        email = self.selenium.find_element_by_name('email')
        email.send_keys("nonsense@non.sense")
        submit = self.selenium.find_element_by_id('login-submit')
        submit.click()
        # Once an incorrect email is entered, an alert is shown
        alert = self.selenium.find_element_by_id('bad-email')

        email = self.selenium.find_element_by_name('email')
        email.send_keys("johnny@niu.edu")
        submit = self.selenium.find_element_by_id('login-submit')
        submit.click()

        # Should be redirected to response screen
        self.assertTrue(self.selenium.current_url.endswith("/response_screen/1"))
