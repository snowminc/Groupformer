from django.test import TestCase
from django.urls import reverse
from dbtools.models import *

class DBToolsModelTest(TestCase):
    #test to set up the test functions by adding GroupFormer and Participant objects into the "test" database
    def setUp(self):
        groupform1 = GroupFormer.objects.create(prof_name = "Dr. Benjamin Johnson", prof_email = "bj@umbc.edu",
                                                 class_section = "CMSC341")
        groupform1.save()

        groupform2 = GroupFormer.objects.create(prof_name="Dr. Jeremy Dixon", prof_email="jd@umbc.edu",
                                                 class_section="CMSC202")
        groupform2.save()

        groupform3 = GroupFormer.objects.create(prof_name="Dr. Richard Chang", prof_email="rc@umbc.edu",
                                                 class_section="CMSC441")
        groupform3.save()
        #Adding a group of participants to the ONLY ONE group former
        p1 = addParticipant(groupform1, "Sarah", "sarah@umbc.edu")
        p2 = addParticipant(groupform1, "Tali", "tali@umbc.edu")
        p3 = addParticipant(groupform1, "Kristian", "kristian@umbc.edu")
        p4 = addParticipant(groupform1, "Kyle", "kyle@umbc.edu")
        p5 = addParticipant(groupform1, "Min", "Min@umbc.edu")
        p6 = addParticipant(groupform1, "Morgan", "Morgan@umbc.edu")

    #test that groupformers were added and that they are in the correct order
    def test_groupformer_added(self):
        gfobj = GroupFormer.objects.all()[0]
        self.assertEqual(gfobj.prof_name, "Dr. Benjamin Johnson")

        gfobj = GroupFormer.objects.all()[1]
        self.assertEqual(gfobj.prof_name, "Dr. Jeremy Dixon")

        gfobj = GroupFormer.objects.all()[2]
        self.assertEqual(gfobj.prof_name, "Dr. Richard Chang")

    #checking that all 6 participants are added to the correct group former
    def test_participant_added(self):
        print("\n")
        gfobj = GroupFormer.objects.all()[0]
        self.assertEqual(6, Participant.objects.filter(group_former=gfobj).count())

    #check that for the other 2 group formers, no participants are added
    def test_no_particpant_added(self):
        print("\n")
        gfobj = GroupFormer.objects.all()[1]
        self.assertEqual(0, Participant.objects.filter(group_former=gfobj).count())

        gfobj = GroupFormer.objects.all()[2]
        self.assertEqual(0, Participant.objects.filter(group_former=gfobj).count())

    #check that redirects to the permission denied html since no email is provided to the url
    def test_no_email_given(self):
        gfobj = GroupFormer.objects.all()[0]
        response = self.client.get(reverse('verify_participant', kwargs={"group_former_id":gfobj.pk}))
        # response code for rendering directly is 200
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Permission Denied")

    def test_email_passed_in(self):
        gfobj = GroupFormer.objects.all()[0]
        response = self.client.get(reverse('verify_participant', kwargs={"group_former_id": gfobj.pk}) + "?email=sarah@umbc.edu")
        self.assertEqual(response.status_code, 302)
        #since it is a redirect, a 302 response code just sends the full url that want to redirect too,
        #so need to ask server to redirect to that url if get a response code of 302
        response = self.client.get(response.url)

        # redirect again to log in page
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)

        # response code should be 200 since not performing a redirect, rendering the url directly
        self.assertContains(response, "Log into")

    #test to get an invalid email that is not part of the groupformer
    def test_invalid_email(self):
        gfobj = GroupFormer.objects.all()[0]
        response = self.client.get(reverse('verify_participant', kwargs={"group_former_id": gfobj.pk}) + "?email=invalidemail@umbc.edu")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Permission Denied")

    #test to make sure a 404 is raised for an invalid group former id
    def test_invalid_groupformer(self):
        response = self.client.get(reverse('verify_participant', kwargs={"group_former_id": 2000}))
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        GroupFormer.objects.all().delete()
        Participant.objects.all().delete()
        Attribute.objects.all().delete()
        Project.objects.all().delete()
        attribute_selection.objects.all().delete()
        project_selection.objects.all().delete()






