from django.test import TestCase
from django.urls import reverse


class MinIteration2ResponseScreenTests(TestCase):
    def test_displays_all_projects(self):
        """
        If the page shows all of the arbitrary project inputs (without backend) from views.py, then it passes
        """
        response = self.client.get(reverse('min_iteration2:response_screen'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SomethingProject")
        self.assertContains(response, "OtherProject")
        self.assertContains(response, "Some description about something that has some substance about some of what something entails")

    def test_displays_all_attributes(self):
        """
        If the page shows all of the arbitrary attribute inputs (without backend) from views.py, then it passes
        """
        response = self.client.get(reverse('min_iteration2:response_screen'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How comfortable are you with front-end?")
        self.assertContains(response, "How comfortable are you with back-end?")

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
        

class SeleniumGroupformerList(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/min_iteration2/groupformer_list'))
        first_groupformer = self.selenium.find_element_by_id("groupformer1_submit")
        second_groupformer = self.selenium.find_element_by_id("groupformer2_submit")
        first_groupformer.click()
        second_groupformer.click()
        first_groups = self.selenium.find_element_by_id("groupformer1_groups")
        second_groups = self.selenium.find_element_by_id("groupformer2_groups")

        self.assertTrue("A, B, C" in first_groups.get_attribute("innerHTML"))
        self.assertTrue("1, 2, 3" in first_groups.get_attribute("innerHTML"))
        self.assertTrue("X, Y, Z" in first_groups.get_attribute("innerHTML"))

        self.assertTrue("Q, A, Z" in second_groups.get_attribute("innerHTML"))
        self.assertTrue("G, M, E" in second_groups.get_attribute("innerHTML"))
        self.assertTrue("A, S, D, F" in second_groups.get_attribute("innerHTML"))

        
