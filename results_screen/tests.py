from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from time import sleep

from dbtools.models import *


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
                                                                 part_email="example@email.com")
        gfs[2]['part' + str(i + 1)] = Participant.objects.create(group_former=gfs[2]['gf'], part_name=names[i],
                                                                 part_email="example@email.com")
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

    def test_get_group(self):
        """
        Test that the now non-arbitrary groups still display on the list.
        "Formed groups" are still arbitrary, and act as if retrieved from the back-end group forming algorithm
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id
        gfs2 = gfs[2]['gf'].id

        self.selenium.get(self.live_server_url + reverse('results_screen:results_screen'))

        # Check that there's nothing on the page first
        page_none = self.selenium.find_element_by_tag_name("body").text
        
        self.assertTrue("A, B, C" not in page_none)
        self.assertTrue("1, 2, 3" not in page_none)
        self.assertTrue("X, Y, Z" not in page_none)
        self.assertTrue("Q, A, Z" not in page_none)
        self.assertTrue("G, M, E" not in page_none)
        self.assertTrue("A, S, D, F" not in page_none)

        # Select the first groupformer tab and create groups
        self.selenium.find_element_by_id("tab-{}".format(gfs1)).click()
        self.selenium.find_element_by_id("groupformer{}_submit".format(gfs1)).click()
        self.selenium.find_element_by_id("groupformer{}_groups".format(gfs1))
        page1text = self.selenium.find_element_by_tag_name("body").text

        # Select the second groupformer tab and create groups
        self.selenium.find_element_by_id("tab-{}".format(gfs2)).click()
        self.selenium.find_element_by_id("groupformer{}_submit".format(gfs2)).click()
        self.selenium.find_element_by_id("groupformer{}_groups".format(gfs2))
        page2text = self.selenium.find_element_by_tag_name("body").text

        # Check both pages if they have the right groups showing currently.
        # Using .text instead of .innerHTML to verify what is VISIBLE (.innerHTML includes hidden text as well)
        for page in ((page1text, gfs1), (page2text, gfs2)):
            # Odd groupformer ids will have the ABC group.
            if page[1] % 2:
                self.assertTrue("A, B, C" in page[0])
                self.assertTrue("1, 2, 3" in page[0])
                self.assertTrue("X, Y, Z" in page[0])
                self.assertTrue("Q, A, Z" not in page[0])
                self.assertTrue("G, M, E" not in page[0])
                self.assertTrue("A, S, D, F" not in page[0])
            else:
                self.assertTrue("A, B, C" not in page[0])
                self.assertTrue("1, 2, 3" not in page[0])
                self.assertTrue("X, Y, Z" not in page[0])
                self.assertTrue("Q, A, Z" in page[0])
                self.assertTrue("G, M, E" in page[0])
                self.assertTrue("A, S, D, F" in page[0])