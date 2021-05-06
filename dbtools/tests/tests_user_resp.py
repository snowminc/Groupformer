from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.auth.models import User
from dbtools.models import *


def create_sample_groupformer():
    '''
    function to create a two sample GroupFormers
    :return:
    '''
    User.objects.create_user("bjohn", "ben.johnson@umbc.edu", "MnbHtgUr")
    User.objects.create_user("mchon", "minc1@umbc.edu", "LALALA")
    gfs = {}
    gfs[1] = {}
    gfs[1]['gf'] = addGroupFormer("Min Chon", "minc1@umbc.edu", "34")
    gfs[2] = {}
    gfs[2]['gf'] = addGroupFormer("Ben Johnson", "ben.johnson@umbc.edu", "24")
    return gfs


def create_sample_projects(gfs):
    '''

    :param gfs: takes a set of groupformer objects
    :return: creates some projects for each groupformer
    '''
    gfs[1]['p1'] = Project.objects.create(group_former=gfs[1]['gf'], project_name="Groupformer Tool",
                                          project_description="Create a tool that creates groups!")
    gfs[1]['p2'] = Project.objects.create(group_former=gfs[1]['gf'], project_name="Robot that pees beer",
                                          project_description="Create a modification on a very expensive robot dog!")

    gfs[2]['p1'] = Project.objects.create(group_former=gfs[2]['gf'], project_name="Literally Something",
                                          project_description="Literally Anything!")
    gfs[2]['p2'] = Project.objects.create(group_former=gfs[2]['gf'], project_name="What",
                                          project_description="I dont know.")


def create_sample_attributes(gfs):
    '''
    :param gfs: create some attributes for the first groupformer objects that is passed in
    :return:
    '''
    # Intentionally do not create attributes for second groupformer
    gfs[1]['a1'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Back-End", is_homogenous=False,
                                            is_continuous=True)
    gfs[1]['a2'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Front-End", is_homogenous=True,
                                            is_continuous=True)
    gfs[1]['a3'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Dog Lover", is_homogenous=False,
                                            is_continuous=False)


def create_sample_participants(gfs):
    '''

    :param gfs: takes in a groupformer object, gfs and creates some participants for each one
    :return: it returns the list of names of those part of the groupformer
    '''
    names = ["Min", "Kristian", "Sarah", "Morgan", "Kyle", "Ben", "Eric", "Andrew"]
    for i in range(len(names)):
        gfs[1]['part' + str(i + 1)] = Participant.objects.create(group_former=gfs[1]['gf'], part_name=names[i],
                                                                 part_email=f"{names[i]}@email.com")
        gfs[2]['part' + str(i + 1)] = Participant.objects.create(group_former=gfs[2]['gf'], part_name=names[i],
                                                                 part_email=f"{names[i]}@email.com")
    return names


def create_all_samples():
    '''
    :return: function that creates all the groupformers, sample_projects, attributes and participants and returns
    the groupformer object
    '''
    gfs = create_sample_groupformer()
    create_sample_projects(gfs)
    create_sample_attributes(gfs)
    create_sample_participants(gfs)
    return gfs

# class that tests out the front end to get a users response
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
        self.selenium.get(
            self.live_server_url + reverse('response_screen:login', kwargs={'groupformer_id': groupformer_id}))

        self.selenium.find_element_by_id('email').send_keys("Kristian@email.com")
        self.selenium.find_element_by_id('login-submit').click()

        # Should be redirected to response screen
        self.assertTrue(self.selenium.current_url.endswith(f"/response_screen/{groupformer_id}"))

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
        self.selenium.get(
            self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
        # Select preferences for both projects
        self.selenium.find_element_by_xpath(
            "//select[@id='projForm{}']/option[text()='Very Interested']".format(gfs[1]['p1'].pk)).click()
        self.selenium.find_element_by_xpath(
            "//select[@id='projForm{}']/option[text()='PLEASE NO']".format(gfs[1]['p2'].pk)).click()
        # Select preferences for all attributes
        self.selenium.find_element_by_xpath(
            "//select[@id='attrForm{}']/option[text()='4']".format(gfs[1]['a1'].pk)).click()
        self.selenium.find_element_by_xpath(
            "//select[@id='attrForm{}']/option[text()='2']".format(gfs[1]['a2'].pk)).click()
        self.selenium.find_element_by_xpath(
            "//select[@id='attrForm{}']/option[text()='5 (Most preferred)']".format(gfs[1]['a3'].pk)).click()
        # Select a few students
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Kristian']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Min']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Ben']").click()
        # Submit
        self.selenium.find_element_by_xpath("//button[@id='submitForm']").click()


        #testing that the users responses actually are in the database

        self.assertEqual(len(project_selection.objects.all()), 2)
        self.assertEqual(len(attribute_selection.objects.all()), 3)

        self.assertEqual(gfs[1]['part2'].getProjectChoice(gfs[1]['p1']).value, 5)
        self.assertEqual(gfs[1]['part2'].getProjectChoice(gfs[1]['p2']).value, 1)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a1']).value, 4)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a2']).value, 2)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a3']).value, 5)
        self.assertSetEqual({'Min', 'Kristian', 'Ben'}, {x.part_name for x in gfs[1]['part2'].desired_partner.all()})





