"""Testing participant, group, and response modules"""
from django.test import TestCase
from dbtools.models import *
from .priority import *


class GroupFormerTest(TestCase):
    """Testing database model with priority algorithm"""

    def setUp(self):
        self.gf = addGroupFormer("Petra", "pnadir@umbc.edu", "Grass watching")
        self.gf.addAttribute("Like salad", True, False)
        self.gf.addAttribute("Backend dev", False, False)
        proj2 = addProject(self.gf, "On top of the hill",
                           "This grass needs to be watched")
        self.gf.addParticipant("Joe", "JoeShmoe@aol.com")
        self.gf.addParticipant("BigDog", "bigdogsgottaeat@food.com")

    #answer the questions
        participantAttributeChoice(self.gf.getParticipantByName("Joe"),
            self.gf.getAttribute("Like salad"), 1)
        participantAttributeChoice(self.gf.getParticipantByName("BigDog"),
            self.gf.getAttribute("Like salad"), 5)
        participantAttributeChoice(self.gf.getParticipantByName("Joe"),
            self.gf.getAttribute("Backend dev"), 3)
        participantAttributeChoice(self.gf.getParticipantByName("BigDog"),
            self.gf.getAttribute("Backend dev"), 4)
    #answer project questions
        participantProjectChoice(self.gf.getParticipantByName("BigDog"),
            self.gf.getProject("On top of the hill"), 1)
        participantProjectChoice(self.gf.getParticipantByName("Joe"),
            self.gf.getProject("On top of the hill"), 1)

    def test_get_groupformer(self):
        print(str(self.gf))
    
    def test_get_participant(self):
        part = self.gf.getParticipantByName("BigDog")
        print(str(part))

    def test_get_roster(self):
        roster = self.gf.getRoster()
        print(str(roster))

    def test_get_project_list(self):
        project_list = self.gf.getProjectList()
        print(str(project_list))
    
    def test_get_a_project(self):
        project = self.gf.getProject("On top of the hill")
        print(project)
    
    def test_get_attributes(self):
        attributes = self.gf.getAttributeList()
        print(attributes)

    def test_get_priority_for_participant_for_project(self):
        project = self.gf.getProject("On top of the hill")
        part = self.gf.getParticipantByName("Joe")

        print(part.getProjectChoice(project).value)

    def test_get_group_score(self):
        project = self.gf.getProject("On top of the hill")
        roster = self.gf.getRoster()
        attribute_list = self.gf.getAttributeList()
        print(str(calc_project_priority(project, roster, attribute_list)))
        self.assertEqual(calc_project_priority(project, roster, attribute_list), 2.0)

    def test_shuffle_particpants(self):
        print(list(self.gf.getRoster()))
        print(shuffle_particpants(self.gf))

    def test_get_global_score(self):
        print(calc_optimal_groups(self.gf)[1])

