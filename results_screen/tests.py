from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from time import sleep

from dbtools.models import *
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from prio_alg.tests import RealWorldTest
from prio_alg.priority import calc_optimal_groups


def create_sample_groupformer():
    gfs = {}
    gfs[1] = {}
    gfs[1]['gf'] = GroupFormer.objects.create(prof_name="Min Chon", prof_email="minc1@umbc.edu", class_section="34")
    gfs[2] = {}
    gfs[2]['gf'] = GroupFormer.objects.create(prof_name="Ben Johnson", prof_email="ben.johnson@umbc.edu",
                                              class_section="24")
    return gfs


def create_sample_projects(gfs):
    gfs[1]['p1'] = Project.objects.create(group_former=gfs[1]['gf'], project_name="Groupformer Tool",
                                          project_description="Create a tool that creates groups!")
    gfs[1]['p2'] = Project.objects.create(group_former=gfs[1]['gf'], project_name="Robot that pees beer",
                                          project_description="Create a modification on a very expensive robot dog!")

    gfs[2]['p1'] = Project.objects.create(group_former=gfs[2]['gf'], project_name="Literally Something",
                                          project_description="Literally Anything!")
    gfs[2]['p2'] = Project.objects.create(group_former=gfs[2]['gf'], project_name="What",
                                          project_description="I dont know.")


def create_sample_attributes(gfs):
    # Intentionally do not create attributes for second groupformer
    gfs[1]['a1'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Back-End", is_homogenous=False,
                                            is_continuous=True)
    gfs[1]['a2'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Front-End", is_homogenous=True,
                                            is_continuous=True)
    gfs[1]['a3'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Dog Lover", is_homogenous=False,
                                            is_continuous=False)


def create_sample_participants(gfs):
    names = ["Min", "Kristian", "Sarah", "Morgan", "Kyle", "Ben", "Eric", "Andrew"]
    for i in range(len(names)):
        gfs[1]['part' + str(i + 1)] = Participant.objects.create(group_former=gfs[1]['gf'], part_name=names[i],
                                                                 part_email=names[i] + "@email.com")
        gfs[2]['part' + str(i + 1)] = Participant.objects.create(group_former=gfs[2]['gf'], part_name=names[i],
                                                                 part_email=names[i] + "@email.com")
    return names


def create_all_samples():
    gfs = create_sample_groupformer()
    create_sample_projects(gfs)
    create_sample_attributes(gfs)
    create_sample_participants(gfs)
    return gfs


class SeleniumGroupformerList(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def try_create_account(self):
        self.selenium.get(self.live_server_url + reverse('setup_screen:create_account_screen'))

        self.selenium.find_element_by_id('first_name').send_keys('Min')
        self.selenium.find_element_by_id('last_name').send_keys('CHon')
        self.selenium.find_element_by_id('username').send_keys('minc')
        self.selenium.find_element_by_id('email').send_keys('minc1@umbc.edu')
        self.selenium.find_element_by_id('password').send_keys('pass1234567')
        self.selenium.find_element_by_id('confirm_password').send_keys('pass1234567')

        self.selenium.find_element_by_id('login-submit').click()

    def sign_in(self):
        self.selenium.get(self.live_server_url + reverse('setup_screen:login_screen'))

        self.selenium.find_element_by_id('username').send_keys('minc')
        self.selenium.find_element_by_id('password').send_keys('pass1234567')

        self.selenium.find_element_by_id('login-submit').click()

    def test_get_group(self):
        """
        Test that the now non-arbitrary groups still display on the list.
        """
        self.try_create_account()
        self.sign_in()

        test_obj = RealWorldTest()
        test_obj.setUp()

        gf_id = test_obj.gf.id

        self.selenium.get(self.live_server_url + reverse('results_screen:results_screen'))

        # Check that there's nothing on the page first
        page_none = self.selenium.find_element_by_tag_name("body").text
        
        # Check that the groupformer instance exists on page
        self.assertTrue("CMSC-447-Section 2" in page_none)
        # Check that the groups weren't given yet
        self.assertTrue("Kyle" not in page_none)
        self.assertTrue("Colin" not in page_none)
        self.assertTrue("Jason" not in page_none)
        self.assertTrue("Connor" not in page_none)
        self.assertTrue("Tony" not in page_none)
        self.assertTrue("Faith" not in page_none)
        self.assertTrue("Danielle" not in page_none)
        self.assertTrue("Omar" not in page_none)
        self.assertTrue("Cameron" not in page_none)
        self.assertTrue("Kai" not in page_none)
        self.assertTrue("Adam" not in page_none)
        self.assertTrue("Luke" not in page_none)
        self.assertTrue("Dona" not in page_none)
        self.assertTrue("Swaithi" not in page_none)
        self.assertTrue("Rhea" not in page_none)
        self.assertTrue("Rhiannon" not in page_none)
        self.assertTrue("David" not in page_none)
        self.assertTrue("Jayce" not in page_none)
        self.assertTrue("JoJo" not in page_none)
        self.assertTrue("Mayor" not in page_none)
        self.assertTrue("Kristen" not in page_none)
        self.assertTrue("Destiny" not in page_none)
        self.assertTrue("Megan" not in page_none)
        self.assertTrue("Marzuq" not in page_none)
        self.assertTrue("Baker" not in page_none)

        # Select the groupformer tab and create groups
        self.selenium.find_element_by_id("tab-{}".format(gf_id)).click()
        self.selenium.find_element_by_id("groupformer{}_submit".format(gf_id)).click()
        self.selenium.find_element_by_id("groupformer{}_groups".format(gf_id))

        import time
        time.sleep(20)  # Give time for the algorithm to load the groups

        page_text = self.selenium.find_element_by_tag_name("body").text

        # Now check that every student is assigned to a group and shown on page
        self.assertTrue("Kyle" in page_text)
        self.assertTrue("Colin" in page_text)
        self.assertTrue("Jason" in page_text)
        self.assertTrue("Connor" in page_text)
        self.assertTrue("Tony" in page_text)
        self.assertTrue("Faith" in page_text)
        self.assertTrue("Danielle" in page_text)
        self.assertTrue("Omar" in page_text)
        self.assertTrue("Cameron" in page_text)
        self.assertTrue("Kai" in page_text)
        self.assertTrue("Adam" in page_text)
        self.assertTrue("Luke" in page_text)
        self.assertTrue("Dona" in page_text)
        self.assertTrue("Swaithi" in page_text)
        self.assertTrue("Rhea" in page_text)
        self.assertTrue("Rhiannon" in page_text)
        self.assertTrue("David" in page_text)
        self.assertTrue("Jayce" in page_text)
        self.assertTrue("JoJo" in page_text)
        self.assertTrue("Mayor" in page_text)
        self.assertTrue("Kristen" in page_text)
        self.assertTrue("Destiny" in page_text)
        self.assertTrue("Megan" in page_text)
        self.assertTrue("Marzuq" in page_text)
        self.assertTrue("Baker" in page_text)