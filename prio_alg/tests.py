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
        participantAttributeChoice(self.part1, self.att1, 4)
        participantAttributeChoice(self.part2, self.att1, 5)
        participantAttributeChoice(self.part1, self.att2, 2)
        participantAttributeChoice(self.part2, self.att2, 3)
        participantAttributeChoice(self.part1, self.att3, 1)
        participantAttributeChoice(self.part2, self.att3, 5)
    #answer project questions
        participantProjectChoice(self.part2, self.proj1, 3)
        participantProjectChoice(self.part1, self.proj1, 4)
        participantProjectChoice(self.part2, self.proj2, 5)
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
        self.assertEqual(project, self.gf.getProject("Grass watching"))
    
    def test_get_attributes(self):
        attributes = self.gf.getAttributeList()
        print(attributes)

    def test_get_attribute_value(self):
        aList = self.gf.getAttributeList()

        for att in aList:
            print(att.is_homogenous)

    def test_get_priority_for_participant_for_project(self):
        print(calc_project_priority(self.proj2, self.gf.getRoster(), None))
        #self.assertEqual(self.part1.getProjectChoice(self.proj1).value, float(1.0))

    def test_get_group_score(self):
        project = self.proj1
        roster = self.gf.getRoster()
        attribute_list = self.gf.getAttributeList()
        print(str(calc_project_priority(project, roster, attribute_list)))
        self.assertEqual(calc_project_priority(project, roster, attribute_list), -1.0)

    def test_shuffle_particpants(self):
        roster = list(self.gf.getRoster())
        shuffled_roster = shuffle_list(list(self.gf.getRoster()))
        print(roster)
        print(shuffled_roster)
        self.assertNotEqual(roster, shuffled_roster, "Roster order is different")

    def test_get_global_score(self):
        groups = create_random_candidate_groups(self.gf, 1)
        print(groups)
        print(str(calc_global_score(groups, self.gf.getAttributeList())))
        #self.assertEqual()
        #print(calc_global_score)
        #print(calc_optimal_groups(self.gf))
    
    def test_desired_partner(self):
        #print the score before making desired partners
        #groups = create_random_candidate_groups(self.gf, 2)
        #print(str(calc_global_score(groups, self.gf.getAttributeList())))
        print('Before adding desiring partners')
        prio1 = calc_project_priority(self.proj1, self.gf.getRoster(), self.gf.getAttributeList())
        print(str(prio1))
        #self.assertEqual(prio, 2.0)
        #print the score after making desired partners
        print('After adding desired partners')
        self.part1.desires(self.part2)
        self.part2.desires(self.part1)
        #print(self.part1.getDesiredPartnerList())
        #self.part2.desires(self.part1)
        #if self.part2 in self.part1.getDesiredPartnerList():
         #   print(True)
        #else:
         #   print(False)
        #print(list(self.part1.desired_partner.all()))
        prio2 = calc_project_priority(self.proj1, self.gf.getRoster(), self.gf.getAttributeList())
        print(str(prio2))
        self.assertGreater(prio2, prio1)

        #print(str(calc_global_score(groups, self.gf.getAttributeList())))

    def test_range_fcn(self):
        min_num = -2
        max_num = 20
        self.assertEqual(max_range(min_num, 2, max_num), 18)
        self.assertEqual(max_range(min_num, 10, max_num), 12)
        self.assertEqual(max_range(min_num, 20, max_num), 22)
    
    def test_create_random_candidates(self):
        print(create_random_candidate_groups(self.gf, 1))
    def test_equal_proj_equal_participants(self):
        print(calc_optimal_groups(self.gf,1))
    def test_more_projects_than_participants(self):
        proj3 = self.gf.addProject("Gardening", "Garden all the vegetables!")
        proj4 = self.gf.addProject("Photograph birds", "Take pictures of birds")
        proj5 = self.gf.addProject("Wood working", "Work all the wood")
        proj6 = self.gf.addProject("Pet big dogs", "Pet all the puppies")

        participantProjectChoice(self.part1, proj3, 2)
        participantProjectChoice(self.part1, proj4, 4)
        participantProjectChoice(self.part1, proj5, 3)
        participantProjectChoice(self.part1, proj6, 4)

        participantProjectChoice(self.part2, proj3, 3)
        participantProjectChoice(self.part2, proj4, 1)
        participantProjectChoice(self.part2, proj5, 5)
        participantProjectChoice(self.part2, proj6, 4)

        print(calc_optimal_groups(self.gf, 1, 1))

        


    def test_max_part_more_than_projects(self):
        pass
    
    def test_equal_participants_to_projects(self):
        pass
    
    def test_less_than_full_projects(self):
        pass