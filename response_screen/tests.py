from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import LiveServerTestCase
from time import sleep
from selenium.webdriver.firefox.webdriver import WebDriver

from dbtools.models import *


def create_sample_groupformer():
    User.objects.create_user("mchon", "minc1@umbc.edu", "pahKygvg")
    User.objects.create_user("bjohn", "ben.johnson@umbc.edu", "MnbHtgUr")
    gfs = {}
    gfs[1] = {}
    gfs[1]['gf'] = addGroupFormer("Min Chon", "minc1@umbc.edu", "34")
    gfs[2] = {}
    gfs[2]['gf'] = addGroupFormer("Ben Johnson", "ben.johnson@umbc.edu", "24")
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
        gfs[1]['part'+str(i+1)] = Participant.objects.create(group_former=gfs[1]['gf'], part_name=names[i], part_email=f"{names[i]}@email.com")
        gfs[2]['part'+str(i+1)] = Participant.objects.create(group_former=gfs[2]['gf'], part_name=names[i], part_email=f"{names[i]}@email.com")
    return names


def create_all_samples():
    gfs = create_sample_groupformer()
    create_sample_projects(gfs)
    create_sample_attributes(gfs)
    create_sample_participants(gfs)
    return gfs


class MinIteration3ResponseScreenTests(TestCase):

    def login_to_sample_groupformer(self):
        self.client.post(reverse('response_screen:login', kwargs={"groupformer_id": 1}), {"email": "Kristian@email.com"})

    def test_displays_all_projects(self):
        """
        Check if the projects created appear on the form
        """
        create_all_samples()
        self.login_to_sample_groupformer()
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
        self.login_to_sample_groupformer()
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
        self.login_to_sample_groupformer()
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
        self.login_to_sample_groupformer()
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
        self.login_to_sample_groupformer()
        response = self.client.get(reverse('response_screen:response_screen', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_displays_participants(self):
        """
        Test that the form lists EVERY participant in the preference selection box
        """
        gfs = create_sample_groupformer()
        names = create_sample_participants(gfs)
        self.login_to_sample_groupformer()
        response1 = self.client.get(reverse('response_screen:response_screen', args=(1,)))
        response2 = self.client.get(reverse('response_screen:response_screen', args=(2,)))
        for i in range(len(names)):
            self.assertContains(response1, names[i])
            self.assertContains(response2, names[i])


class SeleniumResponseScreen(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(1)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def login_to_sample_groupformer(self, groupformer_id):
        self.selenium.get(self.live_server_url + reverse('response_screen:login', kwargs={'groupformer_id': groupformer_id}))

        self.selenium.find_element_by_id('email').send_keys("Kristian@email.com")
        self.selenium.find_element_by_id('login-submit').click()

        # Should be redirected to response screen
        self.assertTrue(self.selenium.current_url.endswith(f"/response_screen/{groupformer_id}"))

    def test_missing_projects_preference(self):
        """
        Test if the error message shows if user does not input a preference for a project.
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id

        self.login_to_sample_groupformer(gfs1)
        # Test for the first groupformer object
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
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

        self.login_to_sample_groupformer(gfs1)
        # Test for the first groupformer object
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
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

        self.login_to_sample_groupformer(gfs1)
        # Test for the first groupformer object
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
        # Remove user info to test missing error
        #self.selenium.find_element_by_xpath("//select[@id='projForm1']/option[text()='Very Interested']").click()
        #self.selenium.find_element_by_xpath("//select[@id='projForm2']/option[text()='PLEASE NO']").click()
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

        proj1_error_message = self.selenium.find_element_by_id(f"projForm{gfs[1]['p1'].pk}_error")
        proj2_error_message = self.selenium.find_element_by_id(f"projForm{gfs[1]['p2'].pk}_error")
        # Using .text instead of .get_attribute("innerHTML") because innerHTML still contains the error, but is hidden
        #  on display. .text only shows what the user sees (ignores any `display: hidden` text)
        self.assertTrue("Must select a preference for this project." in proj1_error_message.text)
        self.assertTrue("Must select a preference for this project." in proj2_error_message.text)


    def test_missing_participant(self):
        """
        Test if the form still successfuly submits on missing participants (it is not a required input)
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id

        self.login_to_sample_groupformer(gfs1)
        # Test for the first groupformer object
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
        # Select preferences for both projects
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='Very Interested']".format(gfs[1]['p1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='PLEASE NO']".format(gfs[1]['p2'].pk)).click()
        # Select preferences for all attributes
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='4']".format(gfs[1]['a1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='2']".format(gfs[1]['a2'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='5 (Most preferred)']".format(gfs[1]['a3'].pk)).click()

        # Select no students
        #self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Kristian']").click()
        #self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Min']").click()
        #self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Ben']").click()

        # Submit
        self.selenium.find_element_by_xpath("//button[@id='submitForm']").click()

        # # Currently, the form is set to post parameters in the URL.
        # url = self.selenium.current_url
        # # Isolate the parameters of the POSTed form
        # param_url = url.rsplit('?', 1)[1]
        # params = param_url.split("&")
        # for i in range(len(params)):
        #     # Replace symbol placeholders with correct character
        #     params[i] = params[i].replace("%20", " ")
        #     params[i] = params[i].replace("+", " ")
        #     params[i] = params[i].replace("%40", "@")
        #     # Create name, value pairs
        #     params[i] = tuple(params[i].split("="))
        #
        # # For each attribute form, the homogenous/continuous values are a hidden form retrieved from the model.
        # # Check if those attributes carried over the correct values for those model objects.
        # self.assertEqual(len(params), 6)  # Check that only the following 5 tuples exist (plus CSRF token)
        # self.assertTrue(('projForm{}_preference'.format(gfs[1]['p1'].pk), '5') in params)
        # self.assertTrue(('projForm{}_preference'.format(gfs[1]['p2'].pk), '1') in params)
        # self.assertTrue(('attrForm{}_preference'.format(gfs[1]['a1'].pk), '4') in params)
        # self.assertTrue(('attrForm{}_preference'.format(gfs[1]['a2'].pk), '2') in params)
        # self.assertTrue(('attrForm{}_preference'.format(gfs[1]['a3'].pk), '5') in params)

        self.assertEqual(len(project_selection.objects.all()), 2)
        self.assertEqual(len(attribute_selection.objects.all()), 3)

        self.assertEqual(gfs[1]['part2'].getProjectChoice(gfs[1]['p1']).value, 5)
        self.assertEqual(gfs[1]['part2'].getProjectChoice(gfs[1]['p2']).value, 1)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a1']).value, 4)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a2']).value, 2)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a3']).value, 5)


    def test_fill_response_screen(self):
        """
        Test that users are required to input important fields such as Name, Email, and all preference boxes
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id
        gfs2 = gfs[2]['gf'].id

        self.login_to_sample_groupformer(gfs1)
        #########################################
        # Test for the first groupformer object #
        #########################################
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
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

        # Currently, the form is set to post parameters in the URL.
        self.assertEqual(len(project_selection.objects.all()), 2)
        self.assertEqual(len(attribute_selection.objects.all()), 3)

        self.assertEqual(gfs[1]['part2'].getProjectChoice(gfs[1]['p1']).value, 5)
        self.assertEqual(gfs[1]['part2'].getProjectChoice(gfs[1]['p2']).value, 1)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a1']).value, 4)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a2']).value, 2)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a3']).value, 5)
        self.assertSetEqual({'Min', 'Kristian', 'Ben'}, {x.part_name for x in gfs[1]['part2'].desired_partner.all()})

        ##########################################
        # Test for the second groupformer object #
        ##########################################
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs2}))
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

        # # Currently, the form is set to post parameters in the URL.
        # url = self.selenium.current_url
        # # Isolate the parameters of the POSTed form
        # param_url = url.rsplit('?', 1)[1]
        # params = param_url.split("&")
        # for i in range(len(params)):
        #     # Replace symbol placeholders with correct character
        #     params[i] = params[i].replace("%20", " ")
        #     params[i] = params[i].replace("+", " ")
        #     params[i] = params[i].replace("%40", "@")
        #     # Create name, value pairs
        #     params[i] = tuple(params[i].split("="))
        #
        # # Attributes do not exist on this Groupformer instance, do not check for them
        # self.assertEqual(len(params), 6)  # Check that only the following 5 tuples exist (plus CSRF token)
        # self.assertTrue(('projForm{}_preference'.format(gfs[2]['p1'].pk), '3') in params)
        # self.assertTrue(('projForm{}_preference'.format(gfs[2]['p2'].pk), '4') in params)
        # self.assertTrue(('participantForm_preference', 'Sarah') in params)
        # self.assertTrue(('participantForm_preference', 'Kyle') in params)
        # self.assertTrue(('participantForm_preference', 'Morgan') in params)
        self.assertEqual(len(project_selection.objects.all()), 4)
        self.assertEqual(len(attribute_selection.objects.all()), 3)

        self.assertEqual(gfs[2]['part2'].getProjectChoice(gfs[2]['p1']).value, 3)
        self.assertEqual(gfs[2]['part2'].getProjectChoice(gfs[2]['p2']).value, 4)
        self.assertSetEqual({'Sarah', 'Kyle', 'Morgan'}, {x.part_name for x in gfs[2]['part2'].desired_partner.all()})


    def test_modal_shows_success(self):
        """
        Test that the modal shows on successful submission
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id

        self.login_to_sample_groupformer(gfs1)
        #########################################
        # Test for the first groupformer object #
        #########################################
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
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
        sleep(1)
        # Check the Modal
        # .text only grabs VISIBLE text
        modal_content = self.selenium.find_element_by_xpath("//div[@id='submitSuccessModalContent']").text

        # Project preferences
        self.assertTrue(gfs[1]['p1'].project_name in modal_content)
        self.assertTrue("5" in modal_content)
        self.assertTrue(gfs[1]['p2'].project_name in modal_content)
        self.assertTrue("1" in modal_content)

        # Attribute preferences
        self.assertTrue(gfs[1]['a1'].attr_name in modal_content)
        self.assertTrue("4" in modal_content)
        self.assertTrue(gfs[1]['a2'].attr_name in modal_content)
        self.assertTrue("2" in modal_content)
        self.assertTrue(gfs[1]['a3'].attr_name in modal_content)
        self.assertTrue("5" in modal_content)

        # Participants listed
        self.assertTrue("Kristian" in modal_content)
        self.assertTrue("Min" in modal_content)
        self.assertTrue("Ben" in modal_content)


    def test_modal_shows_failure(self):
        """
        Test that the modal does not show if the submission was a failure
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id

        self.login_to_sample_groupformer(gfs1)
        #########################################
        # Test for the first groupformer object #
        #########################################
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
        # Select preferences for both projects
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='Very Interested']".format(gfs[1]['p1'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='projForm{}']/option[text()='PLEASE NO']".format(gfs[1]['p2'].pk)).click()
        # Select preferences for all attributes
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='4']".format(gfs[1]['a1'].pk)).click()
        #self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='2']".format(gfs[1]['a2'].pk)).click()
        self.selenium.find_element_by_xpath("//select[@id='attrForm{}']/option[text()='5 (Most preferred)']".format(gfs[1]['a3'].pk)).click()
        # Select a few students
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Kristian']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Min']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Ben']").click()
        # Submit
        self.selenium.find_element_by_xpath("//button[@id='submitForm']").click()

        # Check the Modal
        # .text only grabs VISIBLE text
        modal_title = self.selenium.find_element_by_xpath("//h5[@id='submitSuccessModalLabel']").text

        self.assertFalse("Your response has been submitted!" in modal_title)


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from dbtools.models import *


class LoginScreenTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(1)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        User.objects.create_user("bjohn","bjohn@umbc.edu","eYnNtTBH")
        self.gf = addGroupFormer("Ben Johnson", "bjohn@umbc.edu", "CMSC 447-01")
        self.gf.addParticipant("John Beachy", "johnny@niu.edu")

    def test_login(self):
        self.selenium.get(self.live_server_url + reverse('response_screen:login', kwargs={'groupformer_id': self.gf.pk}))

        # No alert on first look
        with self.assertRaises(NoSuchElementException):
            alert = self.selenium.find_element_by_id('bad-email')

        email = self.selenium.find_element_by_id('email')
        email.send_keys("nonsense@non.sense")
        submit = self.selenium.find_element_by_id('login-submit')
        submit.click()
        # Once an incorrect email is entered, an alert is shown
        alert = self.selenium.find_element_by_id('bad-email')

        email = self.selenium.find_element_by_id('email')
        email.send_keys("johnny@niu.edu")
        submit = self.selenium.find_element_by_id('login-submit')
        submit.click()

        # Should be redirected to response screen
        self.assertTrue(self.selenium.current_url.endswith(f"/response_screen/{self.gf.pk}"))

    def test_redirect_login(self):
        self.selenium.get(self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': self.gf.pk}))

        # Should be redirected to login screen
        self.assertTrue(self.selenium.current_url.endswith(f"/response_screen/{self.gf.pk}/login"))

        email = self.selenium.find_element_by_id('email')
        email.send_keys("johnny@niu.edu")
        submit = self.selenium.find_element_by_id('login-submit')
        submit.click()

        # Should be redirected to response screen
        self.assertTrue(self.selenium.current_url.endswith(f"/response_screen/{self.gf.pk}"))

    def test_login_logout_sequence(self):
        self.selenium.get(self.live_server_url + reverse('response_screen:login', kwargs={'groupformer_id': self.gf.pk}))

        email = self.selenium.find_element_by_id('email')
        email.send_keys("johnny@niu.edu")
        submit = self.selenium.find_element_by_id('login-submit')
        submit.click()

        # Should be redirected to response screen
        self.assertTrue(self.selenium.current_url.endswith(f"/response_screen/{self.gf.pk}"))

        self.selenium.find_element_by_id('logout-link').click()

        # Logging out redirects to login afterwards
        self.assertTrue(self.selenium.current_url.endswith(f"/response_screen/{self.gf.pk}/login"))