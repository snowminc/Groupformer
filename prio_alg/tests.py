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
        val = calc_project_priority(self.proj1, self.gf.getRoster(), None)
        self.assertEqual(val, 7.0)

    def test_get_group_score(self):
        project = self.proj1
        roster = self.gf.getRoster()
        attribute_list = self.gf.getAttributeList()
        self.assertEqual(calc_project_priority(project, roster, attribute_list), -1.0)

    def test_shuffle_particpants(self):
        roster = list(self.gf.getRoster())
        shuffled_roster = shuffle_list(list(self.gf.getRoster()))
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
        print('After adding desired partners')
        self.part1.desires(self.part2)
        self.part2.desires(self.part1)
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

        optimal_groups, second_optimal, third_optimal = calc_optimal_groups(self.gf, 1, 1)

        self.assertEqual(optimal_groups,)

    def test_max_part_more_than_projects(self):
        pass
    
    def test_equal_participants_to_projects(self):
        pass
    
    def test_less_than_full_projects(self):
        pass

class OptimalGroupsTest(TestCase):
    def setUp(self):
        #groupformer creation
        self.gf = addGroupFormer("Ben Johnson", "bjohnson@umbc.edu", "Johnson's project tests")

        #participant creation
        self.part1 = self.gf.addParticipant("Jim", "jimmyneutron@gmail.com")
        self.part2 = self.gf.addParticipant("Jill", "jackandjill@yahoo.com")
        self.part3 = self.gf.addParticipant("Bob", "bigbob@umbc.edu")
        self.part4 = self.gf.addParticipant("Alice", "aliceinwonderland@aol.com")

        #project creation
        self.proj1 = self.gf.addProject("proj1", "proj description")
        self.proj2 = self.gf.addProject("proj2", "proj description")

        #attribute creation
        self.att1 = self.gf.addAttribute("backend", False, False)
        self.att2 = self.gf.addAttribute("likes video games", True, False)

        #project answers
        participantProjectChoice(self.part1, self.proj1, 5)
        participantProjectChoice(self.part1, self.proj2, 1)
        participantProjectChoice(self.part2, self.proj1, 3)
        participantProjectChoice(self.part2, self.proj2, 3)
        participantProjectChoice(self.part3, self.proj1, 3)
        participantProjectChoice(self.part3, self.proj2, 3)
        participantProjectChoice(self.part4, self.proj1, 2)
        participantProjectChoice(self.part4, self.proj2, 2)

        #attribute answers
        participantAttributeChoice(self.part1, self.att1, 5)
        participantAttributeChoice(self.part1, self.att2, 1)
        participantAttributeChoice(self.part2, self.att1, 1)
        participantAttributeChoice(self.part2, self.att2, 3)
        participantAttributeChoice(self.part3, self.att1, 4)
        participantAttributeChoice(self.part3, self.att2, 3)
        participantAttributeChoice(self.part4, self.att1, 2)
        participantAttributeChoice(self.part4, self.att2, 1)

    def test_calc_priority(self):
        roster = [self.part1, self.part4]
        roster2 = [self.part2, self.part3]
        self.assertEqual(calc_project_priority(self.proj1, roster, self.gf.getAttributeList()), 10)
        self.assertEqual(calc_project_priority(self.proj2, roster2, self.gf.getAttributeList()), 9)
    def test_get_optimal_group(self):
        best_group, second_group, third_group = calc_optimal_groups(self.gf, 2)
        #self.assert that the particpants are jim / alice in proj1, bob / jill in proj2
        self.assertEqual(best_group[1], 28, 'The best group value is indeed 28!')
        
    def test_get_multiple_optimal_groups(self):
        best_group, second_group, third_group = calc_optimal_groups(self.gf, 2)
        self.assertEqual(best_group[1], 28, 'The best group value is indeed 28!')
        self.assertEqual(second_group[1], 21, 'The second best value is 21!')
        self.assertEqual(third_group[1], 20, 'The third best value is 20!')

    def test_get_priority_for_participant_for_project(self):
        val = calc_project_priority(self.proj1, self.gf.getRoster(), None)
        self.assertEqual(val, 13.0)

    def test_desired_partner(self):
        # print the score before making desired partners
        # groups = create_random_candidate_groups(self.gf, 2)
        # print(str(calc_global_score(groups, self.gf.getAttributeList())))
        print('Before adding desiring partners')
        best_group, second_group, third_group = calc_optimal_groups(self.gf, 2)
        print(str(best_group))
        print('After adding desired partners')
        self.part1.desires(self.part1)
        self.part2.desires(self.part4)
        best_group2, second_group, third_group = calc_optimal_groups(self.gf, 2)
        print(str(best_group2))
        self.assertGreater(best_group2[1], best_group[1])
    
