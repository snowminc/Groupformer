from django.test import TestCase
from django.urls import reverse
from dbtools.models import *

class DBToolsModelTest(TestCase):
    #test to set up the test functions by adding Project Objects into the "test" database
    def setUp(self):
        groupform1 = GroupFormer.objects.create(prof_name = "Dr. Benjamin Johnson", prof_email = "bj@umbc.edu",
                                                 class_section = "CMSC341")
        groupform1.save()

        groupform2 = GroupFormer.objects.create(prof_name="Dr. Jeremy Dixon", prof_email="jd@umbc.edu",
                                                 class_section="CMSC202")
        groupform2.save()

        groupform3 = GroupFormer.objects.create(prof_name="Dr. Richard Chang", prof_email="bj@umbc.edu",
                                                 class_section="CMSC441")
        groupform3.save()
        p1 = addParticipant(groupform1, "Sarah", "sarah@umbc.edu")
        p2 = addParticipant(groupform1, "Tali", "tali@umbc.edu")
        p3 = addParticipant(groupform1, "Kristian", "kristian@umbc.edu")
        p4 = addParticipant(groupform1, "Kyle", "kyle@umbc.edu")
        p5 = addParticipant(groupform1, "Min", "Min@umbc.edu")
        p6 = addParticipant(groupform1, "Morgan", "Morgan@umbc.edu")

    def test_groupformer_added(self):
        gfobj = GroupFormer.objects.all()[0]
        self.assertEqual(gfobj.prof_name, "Dr. Benjamin Johnson")

        gfobj = GroupFormer.objects.all()[1]
        self.assertEqual(gfobj.prof_name, "Dr. Jeremy Dixon")

        gfobj = GroupFormer.objects.all()[2]
        self.assertEqual(gfobj.prof_name, "Dr. Richard Chang")

    def test_participant_added(self):
        print("\n")
        gfobj = GroupFormer.objects.all()[0]
        self.assertEqual(6, Participant.objects.filter(group_former=gfobj).count())

    def test_no_particpant_added(self):
        print("\n")
        gfobj = GroupFormer.objects.all()[1]
        self.assertEqual(0, Participant.objects.filter(group_former=gfobj).count())


    def testing_verify_participant_view(self):
        response = self.client.get(reverse('verify_participant'))
        self.assertEqual(response.status_code, 200)




