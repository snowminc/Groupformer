"""Testing participant, group, and response modules"""
from django.test import TestCase
from dbtools.models import *
from .priority import *


class GroupFormerTest(TestCase):
    """Testing database model with priority algorithm"""

    def setUp(self):
        self.gf = addGroupFormer("Petra", "pnadir@umbc.edu", "Petra's Project Tests")
        self.att1 = self.gf.addAttribute("Like salad", True, False)
        self.att2 = self.gf.addAttribute("Backend dev", False, False)
        self.att3 = self.gf.addAttribute("Do you like watching videos until 3 am?", True, False)
        self.proj1 = self.gf.addProject("Grass watching",
                           "This grass needs to be watched")
        self.proj2 = self.gf.addProject("Gaming on a budget", "How do you game on a budget??")
        self.part1 = self.gf.addParticipant("Joe", "JoeShmoe@aol.com")
        self.part2 = self.gf.addParticipant("BigDog", "bigdogsgottaeat@food.com")

    #answer the questions
        participantAttributeChoice(self.part1, self.att1, 1)
        participantAttributeChoice(self.part2, self.att1, 5)
        participantAttributeChoice(self.part1, self.att2, 3)
        participantAttributeChoice(self.part2, self.att2, 4)
        participantAttributeChoice(self.part1, self.att3, 4)
        participantAttributeChoice(self.part2, self.att3, 4)
    #answer project questions
        participantProjectChoice(self.part2, self.proj1, 1)
        participantProjectChoice(self.part1, self.proj1, 1)
        participantProjectChoice(self.part2, self.proj2, 4)
        participantProjectChoice(self.part1, self.proj2, 5)

    def test_get_groupformer(self):
        print(str(self.gf))
        self.assertEqual(getGroupFormer("Petra", "Petra's Project Tests"), self.gf)
    
    def test_get_participant(self):
        part = self.gf.getParticipantByName("BigDog")
        print(str(part))
        self.assertEqual(getGroupFormer("Petra", "Petra's Project Tests").getParticipantByName("BigDog"), part)


    def test_get_roster(self):
        roster = self.gf.getRoster()
        print(str(roster))
        l = [ self.gf.getParticipantByName("Joe"), self.gf.getParticipantByName("BigDog") ]
        self.assertEqual(list(roster), l)

    def test_get_project_list(self):
        project_list = self.gf.getProjectList()
        print(str(project_list))
        alist = [ self.proj1, self.proj2 ]
        self.assertEqual(list(project_list), alist, "Test passed")
    
    def test_get_a_project(self):
        project = self.proj1
        print(project)
    
    def test_get_attributes(self):
        attributes = self.gf.getAttributeList()
        print(attributes)

    def test_get_priority_for_participant_for_project(self):
        self.assertEqual(self.part1.getProjectChoice(self.proj1).value, float(1.0))

    def test_get_group_score(self):
        project = self.proj1
        roster = self.gf.getRoster()
        attribute_list = self.gf.getAttributeList()
        print(str(calc_project_priority(project, roster, attribute_list)))
        self.assertEqual(calc_project_priority(project, roster, attribute_list), 2.0)

    def test_shuffle_particpants(self):
        roster = list(self.gf.getRoster())
        shuffled_roster = shuffle_list(list(self.gf.getRoster()))
        print(roster)
        print(shuffled_roster)
        self.assertNotEqual(roster, shuffled_roster, "Roster order is different")

    def test_get_global_score(self):
        groups = create_random_candidate_groups(self.gf, 1)
        print(groups)
        #self.assertEqual()
        #print(calc_global_score)
        #print(calc_optimal_groups(self.gf))
    
    def test_desired_partner(self):
        #print the score before making desired partners
        groups = create_random_candidate_groups(self.gf, 1)
        print(str(calc_global_score(groups, self.gf.getAttributeList())))
        #print the score after making desired partners
        self.part1.desires(self.part2)
        self.part2.desires(self.part1)

        print(str(calc_global_score(groups, self.gf.getAttributeList())))

