from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from dbtools.models import *

class DBToolsRecordResponseTest(TestCase):

    #set up a group former, with participants, attributes and projects
    def setUp(self):
        '''
        function that sets up the test database with participants, attributes and projects
        :return:
        '''
        User.objects.create_user("ben", "b@umbc.edu", "MnbHtgUr")
        self.groupform1 = addGroupFormer("ben", "b@umbc.edu", "24")
        self.groupform1.save()

        #add participants
        self.p1 = addParticipant(self.groupform1, "S", "s@umbc.edu")
        self.p2 = addParticipant(self.groupform1, "T", "t@umbc.edu")
        self.p3 = addParticipant(self.groupform1, "Kr", "kr@umbc.edu")
        self.p4 = addParticipant(self.groupform1, "Ky", "ky@umbc.edu")
        self.p5 = addParticipant(self.groupform1, "Mi", "Mi@umbc.edu")
        self.p6 = addParticipant(self.groupform1, "Mo", "Mo@umbc.edu")

        #add projects
        self.proj1 = addProject(self.groupform1, "Project1Name", "project1 Description")
        self.proj2 = addProject(self.groupform1, "Project2Name", "project2 Description")
        self.proj3 = addProject(self.groupform1, "Project3Name", "project3 Description")
        self.proj4 = addProject(self.groupform1, "Project4Name", "project4 Description")

        #add attributes
        self.attr1 = addAttribute(self.groupform1, "An Attribute1", False, False)
        self.attr2 = addAttribute(self.groupform1, "An Attribute2", False, False)

    def tearDown(cls):
        '''
         function tears down the test database after the test is completed
        :return:
        '''
        GroupFormer.objects.all().delete()
        Participant.objects.all().delete()
        Attribute.objects.all().delete()
        Project.objects.all().delete()
        attribute_selection.objects.all().delete()
        project_selection.objects.all().delete()

    def test_groupformer_added(self):
        '''
        function tests that a groupformer was added to the test database
        :return:
        '''
        gfobj = GroupFormer.objects.all()[0]
        self.assertEqual(gfobj.prof_name, "ben")


    def test_participant_added(self):
        '''
        function tests that participants were added to the database
        :return:
        '''
        gfobj = GroupFormer.objects.all()[0]
        self.assertEqual(6, Participant.objects.filter(group_former=gfobj).count())


    def test_attributes_added(self):
        '''
        function tests that attributes were added to the database
        :return:
        '''
        print("\n")
        gfobj = GroupFormer.objects.all()[0]
        self.assertEqual(2, Attribute.objects.filter(group_former=gfobj).count())


    def no_responses(self):
        '''
        function that tests that no response are already stored in the database
        :return:
        '''
        self.assertEqual(len(project_selection.objects.all()), 0)
        self.assertEqual(len(attribute_selection.objects.all()), 0)

        projects = Project.objects.all()
        for proj in projects:
            self.assertEqual(len(proj.desired_partner), 0)

    def test_saved_response(self):
        '''
        test to check that a participants project and attributes are saved into the database
        :return:
        '''
        response_dict = {
                        "participantNameForm": self.p1.part_name,
                        "participantEmailForm": self.p1.part_email,
                        f"projForm{self.proj1.id}_preference": 1,
                        f"projForm{self.proj2.id}_preference": 2,
                        f"projForm{self.proj3.id}_preference": 3,
                        f"projForm{self.proj4.id}_preference": 4,
                        f"attrForm{self.attr1.id}_preference": 1,
                        f"attrForm{self.attr2.id}_preference": 2,
        }

        response = self.client.post(reverse('dbtools:record_response', kwargs={"group_former_id": self.groupform1.pk}), response_dict)
        self.assertEqual(response.status_code, 200)

        #correct amount of project and attribute selections are in the database
        self.assertEqual(len(project_selection.objects.all()), 4)
        self.assertEqual(len(attribute_selection.objects.all()), 2)

        #check that the right values are recorded in the database
        self.assertEqual(self.p1.getProjectChoice(self.proj1).value, 1)
        self.assertEqual(self.p1.getProjectChoice(self.proj2).value, 2)
        self.assertEqual(self.p1.getProjectChoice(self.proj3).value, 3)
        self.assertEqual(self.p1.getProjectChoice(self.proj4).value, 4)
        self.assertEqual(self.p1.getAttributeChoice(self.attr1).value, 1)
        self.assertEqual(self.p1.getAttributeChoice(self.attr2).value, 2)


    def test_saved_response_withpartners(self):
        '''
        test to check that if a participant desires to work with other participants, it is properly recorded
        :return:
        '''
        response_dict = {
            "participantNameForm": self.p3.part_name,
            "participantEmailForm": self.p3.part_email,
            f"projForm{self.proj1.id}_preference": 1,
            f"projForm{self.proj2.id}_preference": 1,
            f"projForm{self.proj3.id}_preference": 1,
            f"projForm{self.proj4.id}_preference": 1,
            f"attrForm{self.attr1.id}_preference": 1,
            f"attrForm{self.attr2.id}_preference": 1,
            "participantForm_preference": [self.p1.part_name, self.p2.part_name]
        }

        response = self.client.post(reverse('dbtools:record_response', kwargs={"group_former_id": self.groupform1.pk}),  response_dict)
        self.assertEqual(response.status_code, 200)


        self.assertEqual(len(project_selection.objects.all()), 4)
        self.assertEqual(len(attribute_selection.objects.all()), 2)

        self.assertEqual(self.p3.getProjectChoice(self.proj1).value, 1)
        self.assertEqual(self.p3.getProjectChoice(self.proj2).value, 1)
        self.assertEqual(self.p3.getProjectChoice(self.proj3).value, 1)
        self.assertEqual(self.p3.getProjectChoice(self.proj4).value, 1)
        self.assertEqual(self.p3.getAttributeChoice(self.attr1).value, 1)
        self.assertEqual(self.p3.getAttributeChoice(self.attr2).value, 1)
        self.assertSetEqual(set(response_dict["participantForm_preference"]), {x.part_name for x in self.p3.desired_partner.all()})

    def test_method_is_get(self):
        '''
        test that the view only works with a POST
        :return:
        '''
        response = self.client.get(reverse('dbtools:record_response', kwargs={"group_former_id": self.groupform1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_update_response(self):
        '''
        :return: added a test to ensure that a users responses are updated
        '''
        response_dict = {
            "participantNameForm": self.p5.part_name,
            "participantEmailForm": self.p5.part_email,
            f"projForm{self.proj1.id}_preference": 3,
            f"projForm{self.proj2.id}_preference": 3,
            f"projForm{self.proj3.id}_preference": 3,
            f"projForm{self.proj4.id}_preference": 3,
            f"attrForm{self.attr1.id}_preference": 3,
            f"attrForm{self.attr2.id}_preference": 3,
            "participantForm_preference": [self.p1.part_name, self.p2.part_name]
        }

        response = self.client.post(reverse('dbtools:record_response', kwargs={"group_former_id": self.groupform1.pk}),
                                    response_dict)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(project_selection.objects.all()), 4)
        self.assertEqual(len(attribute_selection.objects.all()), 2)

        self.assertEqual(self.p5.getProjectChoice(self.proj1).value, 3)
        self.assertEqual(self.p5.getProjectChoice(self.proj2).value, 3)
        self.assertEqual(self.p5.getProjectChoice(self.proj3).value, 3)
        self.assertEqual(self.p5.getProjectChoice(self.proj4).value, 3)
        self.assertEqual(self.p5.getAttributeChoice(self.attr1).value, 3)
        self.assertEqual(self.p5.getAttributeChoice(self.attr2).value, 3)
        self.assertSetEqual(set(response_dict["participantForm_preference"]),
                            {x.part_name for x in self.p5.desired_partner.all()})

        response_dict = {
            "participantNameForm": self.p5.part_name,
            "participantEmailForm": self.p5.part_email,
            f"projForm{self.proj1.id}_preference": 2,
            f"projForm{self.proj2.id}_preference": 2,
            f"projForm{self.proj3.id}_preference": 2,
            f"projForm{self.proj4.id}_preference": 2,
            f"attrForm{self.attr1.id}_preference": 2,
            f"attrForm{self.attr2.id}_preference": 2,
            "participantForm_preference": [self.p3.part_name, self.p4.part_name]
        }
        response = self.client.post(reverse('dbtools:record_response', kwargs={"group_former_id": self.groupform1.pk}),
                                    response_dict)
        self.assertEqual(response.status_code, 200)


        self.assertEqual(len(project_selection.objects.all()), 4)
        self.assertEqual(len(attribute_selection.objects.all()), 2)

        self.assertEqual(self.p5.getProjectChoice(self.proj1).value, 2)
        self.assertEqual(self.p5.getProjectChoice(self.proj2).value, 2)
        self.assertEqual(self.p5.getProjectChoice(self.proj3).value, 2)
        self.assertEqual(self.p5.getProjectChoice(self.proj4).value, 2)
        self.assertEqual(self.p5.getAttributeChoice(self.attr1).value, 2)
        self.assertEqual(self.p5.getAttributeChoice(self.attr2).value, 2)
        self.assertSetEqual(set(response_dict["participantForm_preference"]),
                            {x.part_name for x in self.p5.desired_partner.all()})





