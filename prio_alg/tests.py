"""Testing participant, group, and response modules"""
from django.test import TestCase
from dbtools.models import *
from .priority import *


class GroupFormerTest(TestCase):
    """Testing database model with priority algorithm"""


    def setUp(self):
        User.objects.create_user("petra","pnadir@umbc.edu","cmW4NpNh")
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
        self.assertEqual(greater_difference(min_num, 2, max_num), 18)
        self.assertEqual(greater_difference(min_num, 10, max_num), 12)
        self.assertEqual(greater_difference(min_num, 20, max_num), 22)
    
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

        self.assertGreater(optimal_groups[1], second_optimal[1])

    def test_max_part_more_than_projects(self):
        pass
    
    def test_equal_participants_to_projects(self):
        pass
    
    def test_less_than_full_projects(self):
        pass

class OptimalGroupsTest(TestCase):
    def setUp(self):
        #groupformer creation
        User.objects.create_user("bjohn","bjohnson@umbc.edu","UkEHMkqV")
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
    
class RealWorldTest(TestCase):

    def setUp(self):
        User.objects.create_user("bjohn","benj@umbc.edu","UkEHMkqV")
        self.gf = addGroupFormer("Ben Johnson", "benj@umbc.edu", "CMSC-447-Section 2")

        self.proj1 = self.gf.addProject("Data privacy visualization", "This app will allow technological "
                                                                      "laypeople to log in to their various "
                                                                      "social media accounts in order to see "
                                                                      "what information those companies have "
                                                                      "for them. The app will visualize this "
                                                                      "information is an easily understood manner, "
                                                                      "and present suggested interventions for "
                                                                      "the user to \"lock down\" those social "
                                                                      "media accounts. CEO: Ben Johnson "
                                                                      "(your professor)")
        self.proj2 = self.gf.addProject("Real animal pokemon go", "Using the iNaturalist API, this app will "
                                                                  "allow users to take wildlife pictures with "
                                                                  "GPS tags. Once uploaded, those creatures"
                                                                  " are given role-playing game (RPG) stats."
                                                                  " User can use their pets to battle others"
                                                                  " or send them on adventures. The app will"
                                                                  " provide interesting facts to educate users"
                                                                  " on the wildlife they've found. CEO: James"
                                                                  " Stevenson (senior industry software developer")

        self.proj3 = self.gf.addProject("Letter of Recommendation Portal", "This app will allow students to request"
                                                                           " letters of recommendation from"
                                                                           " professors and upload copies of their "
                                                                           "CV/Resume. Professors will be able to "
                                                                           "see what letters they've agreed to "
                                                                           "write organized by due date. "
                                                                           "CEO: Jeremy Dixon (Senior Lecturer)")
        self.proj4 = self.gf.addProject("COVID Lunches", "This app will provide a means for public school students"
                                                         " to receive their school lunches during the COVID-19 "
                                                         "pandemic. The apps tracks which students receive free or"
                                                         " discount lunches, and tracks which students have been able"
                                                         " to collect their lunches each day. CEO: Kristin Sinclair"
                                                         "(Industry Design Director)")

        self.proj5 = self.gf.addProject("Shared Spaces", "This app allows public and private facilities to manage "
                                                         "their seating, and allow users to find places to work,"
                                                         " play or study. Spaces can be advertised by various criteria,"
                                                         " including maximum occupancy, noise level, facilities "
                                                         "(food, restrooms, etc) and wifi availability. "
                                                         "CEO: Ben Johnson ")
        self.proj6 = self.gf.addProject("Dynamic history tours", "This app allows users to find pre-made tours based"
                                                                 " on historical themes. For instance, if you are in"
                                                                 " Baltimore MD and enjoy Edgar Allen Poe, this app"
                                                                 " would provide a self-paced tour of points of "
                                                                 "interest surrounding Poe. The app will also provide a"
                                                                 " means for users to generate tours based on their "
                                                                 "historical knowledge, and knowledge of the modern "
                                                                 "setting. CEO: Ben Johnson")

        self.proj7 = self.gf.addProject("Human Resource Calculator", "This app would allow project managers to "
                                                                     "calculate what staff and time is required for "
                                                                     "large, complex projects. CEO: Kristin Sinclair "
                                                                     "(Industry Design Director)")
        self.proj8 = self.gf.addProject("\"Mystery in a box\" author tool", "This app allows users to write narrative"
                                                                            " mystery games which send players around"
                                                                            " a real or fictitious setting looking for"
                                                                            " clues and leads. The app helps authors "
                                                                            "determine which clues they've offered"
                                                                            " making sure that they mysteries are in "
                                                                            "fact solvable. CEO: Detective Ben Johnson")

        self.proj9 = self.gf.addProject("Group forming tool", "A tool to form 447 groups that isn't a lousy "
                                                              "Google Form. Users will be able to form groups"
                                                              " based on project interest, team role, skill "
                                                              "set, etc. CEO: Ben Johnson")
        self.proj10 = self.gf.addProject("Open Piazza", "An app that provides similar functionality to Piazza,"
                                                        " but can be more greatly customized and individually "
                                                        "managed. CEO: Frank Ferraro (Assistant Professor)")

        self.proj11 = self.gf.addProject("Filmpop", " Film pop supports \"pop up\" drive in theaters. Movie "
                                                    "goers can find movie/show releases playing in their area."
                                                    " They can drive to the location and watch the movie as long "
                                                    "as they remain close to that location. Local businesses can "
                                                    "add movie locations near their business to promote "
                                                    "customer visits. CEO: Kristin Sinclair (Industry Design Director)")
        self.proj12 = self.gf.addProject("The Data Structures Game", "This app allows CMSC 341 Data structures"
                                                                     " students to play games to improve their data"
                                                                     " structures skills and challenge their "
                                                                     "classmates. CEO: Ben Johnson, Senior Developers:"
                                                                     " Naomi Albert, Ryan Barron, Maksim Eren, Nick "
                                                                     "Solovyev. This is the first ever legacy project "
                                                                     "-- you will be building from an existing codebase"
                                                                     " with the help and guidance of the previous "
                                                                     "developers. It doesn't get much more realistic "
                                                                     "than this.")
        self.part1 = self.gf.addParticipant("Kyle", "gs49698@umbc.edu")
        participantProjectChoice(self.part1, self.proj1, 1)
        participantProjectChoice(self.part1, self.proj2, 4)
        participantProjectChoice(self.part1, self.proj3, 5)
        participantProjectChoice(self.part1, self.proj4, 5)
        participantProjectChoice(self.part1, self.proj5, 3)
        participantProjectChoice(self.part1, self.proj6, 2)
        participantProjectChoice(self.part1, self.proj7, 4)
        participantProjectChoice(self.part1, self.proj8, 1)
        participantProjectChoice(self.part1, self.proj9, 5)
        participantProjectChoice(self.part1, self.proj10, 5)
        participantProjectChoice(self.part1, self.proj11, 3)
        participantProjectChoice(self.part1, self.proj12, 3)

        self.part2 = self.gf.addParticipant("Colin", "example1@umbc.edu")
        participantProjectChoice(self.part2, self.proj1, 5)
        participantProjectChoice(self.part2, self.proj2, 5)
        participantProjectChoice(self.part2, self.proj3, 4)
        participantProjectChoice(self.part2, self.proj4, 3)
        participantProjectChoice(self.part2, self.proj5, 4)
        participantProjectChoice(self.part2, self.proj6, 2)
        participantProjectChoice(self.part2, self.proj7, 1)
        participantProjectChoice(self.part2, self.proj8, 1)
        participantProjectChoice(self.part2, self.proj9, 2)
        participantProjectChoice(self.part2, self.proj10, 5)
        participantProjectChoice(self.part2, self.proj11, 3)
        participantProjectChoice(self.part2, self.proj12, 4)
        self.part3 = self.gf.addParticipant("Jason", "example2@umbc.edu")
        participantProjectChoice(self.part3, self.proj1, 4)
        participantProjectChoice(self.part3, self.proj2, 3)
        participantProjectChoice(self.part3, self.proj3, 2)
        participantProjectChoice(self.part3, self.proj4, 2)
        participantProjectChoice(self.part3, self.proj5, 2)
        participantProjectChoice(self.part3, self.proj6, 1)
        participantProjectChoice(self.part3, self.proj7, 4)
        participantProjectChoice(self.part3, self.proj8, 5)
        participantProjectChoice(self.part3, self.proj9, 3)
        participantProjectChoice(self.part3, self.proj10, 3)
        participantProjectChoice(self.part3, self.proj11, 1)
        participantProjectChoice(self.part3, self.proj12, 2)
        self.part4 = self.gf.addParticipant("Connor", "example3@umbc.edu")
        participantProjectChoice(self.part4, self.proj1, 1)
        participantProjectChoice(self.part4, self.proj2, 3)
        participantProjectChoice(self.part4, self.proj3, 5)
        participantProjectChoice(self.part4, self.proj4, 2)
        participantProjectChoice(self.part4, self.proj5, 3)
        participantProjectChoice(self.part4, self.proj6, 1)
        participantProjectChoice(self.part4, self.proj7, 3)
        participantProjectChoice(self.part4, self.proj8, 3)
        participantProjectChoice(self.part4, self.proj9, 3)
        participantProjectChoice(self.part4, self.proj10, 4)
        participantProjectChoice(self.part4, self.proj11, 5)
        participantProjectChoice(self.part4, self.proj12, 4)

        self.part5 = self.gf.addParticipant("Tony", "example4@umbc.edu")
        participantProjectChoice(self.part5, self.proj1, 1)
        participantProjectChoice(self.part5, self.proj2, 2)
        participantProjectChoice(self.part5, self.proj3, 3)
        participantProjectChoice(self.part5, self.proj4, 4)
        participantProjectChoice(self.part5, self.proj5, 5)
        participantProjectChoice(self.part5, self.proj6, 5)
        participantProjectChoice(self.part5, self.proj7, 4)
        participantProjectChoice(self.part5, self.proj8, 3)
        participantProjectChoice(self.part5, self.proj9, 2)
        participantProjectChoice(self.part5, self.proj10, 1)
        participantProjectChoice(self.part5, self.proj11, 2)
        participantProjectChoice(self.part5, self.proj12, 4)
        self.part6 = self.gf.addParticipant("Faith", "example5@umbc.edu")
        participantProjectChoice(self.part6, self.proj1, 1)
        participantProjectChoice(self.part6, self.proj2, 1)
        participantProjectChoice(self.part6, self.proj3, 1)
        participantProjectChoice(self.part6, self.proj4, 2)
        participantProjectChoice(self.part6, self.proj5, 2)
        participantProjectChoice(self.part6, self.proj6, 3)
        participantProjectChoice(self.part6, self.proj7, 4)
        participantProjectChoice(self.part6, self.proj8, 5)
        participantProjectChoice(self.part6, self.proj9, 5)
        participantProjectChoice(self.part6, self.proj10, 5)
        participantProjectChoice(self.part6, self.proj11, 2)
        participantProjectChoice(self.part6, self.proj12, 1)
        self.part7 = self.gf.addParticipant("Danielle", "example6@umbc.edu")
        participantProjectChoice(self.part7, self.proj1, 4)
        participantProjectChoice(self.part7, self.proj2, 4)
        participantProjectChoice(self.part7, self.proj3, 4)
        participantProjectChoice(self.part7, self.proj4, 5)
        participantProjectChoice(self.part7, self.proj5, 3)
        participantProjectChoice(self.part7, self.proj6, 1)
        participantProjectChoice(self.part7, self.proj7, 2)
        participantProjectChoice(self.part7, self.proj8, 2)
        participantProjectChoice(self.part7, self.proj9, 3)
        participantProjectChoice(self.part7, self.proj10, 5)
        participantProjectChoice(self.part7, self.proj11, 5)
        participantProjectChoice(self.part7, self.proj12, 4)

        self.part8 = self.gf.addParticipant("Omar", "example@umbc7.edu")
        participantProjectChoice(self.part8, self.proj1, 2)
        participantProjectChoice(self.part8, self.proj2, 2)
        participantProjectChoice(self.part8, self.proj3, 1)
        participantProjectChoice(self.part8, self.proj4, 2)
        participantProjectChoice(self.part8, self.proj5, 4)
        participantProjectChoice(self.part8, self.proj6, 3)
        participantProjectChoice(self.part8, self.proj7, 3)
        participantProjectChoice(self.part8, self.proj8, 2)
        participantProjectChoice(self.part8, self.proj9, 1)
        participantProjectChoice(self.part8, self.proj10, 5)
        participantProjectChoice(self.part8, self.proj11, 4)
        participantProjectChoice(self.part8, self.proj12, 4)
        self.part9 = self.gf.addParticipant("Cameron", "example@um8bc.edu")
        participantProjectChoice(self.part9, self.proj1, 1)
        participantProjectChoice(self.part9, self.proj2, 4)
        participantProjectChoice(self.part9, self.proj3, 3)
        participantProjectChoice(self.part9, self.proj4, 3)
        participantProjectChoice(self.part9, self.proj5, 4)
        participantProjectChoice(self.part9, self.proj6, 3)
        participantProjectChoice(self.part9, self.proj7, 2)
        participantProjectChoice(self.part9, self.proj8, 5)
        participantProjectChoice(self.part9, self.proj9, 3)
        participantProjectChoice(self.part9, self.proj10, 1)
        participantProjectChoice(self.part9, self.proj11, 2)
        participantProjectChoice(self.part9, self.proj12, 3)
        self.part10 = self.gf.addParticipant("Kai", "example@umbc.e9du")
        participantProjectChoice(self.part10, self.proj1, 2)
        participantProjectChoice(self.part10, self.proj2, 3)
        participantProjectChoice(self.part10, self.proj3, 4)
        participantProjectChoice(self.part10, self.proj4, 4)
        participantProjectChoice(self.part10, self.proj5, 5)
        participantProjectChoice(self.part10, self.proj6, 2)
        participantProjectChoice(self.part10, self.proj7, 1)
        participantProjectChoice(self.part10, self.proj8, 3)
        participantProjectChoice(self.part10, self.proj9, 3)
        participantProjectChoice(self.part10, self.proj10, 5)
        participantProjectChoice(self.part10, self.proj11, 3)
        participantProjectChoice(self.part10, self.proj12, 2)

        self.part11 = self.gf.addParticipant("Adam", "example@umb1c.edu")
        participantProjectChoice(self.part11, self.proj1, 1)
        participantProjectChoice(self.part11, self.proj2, 2)
        participantProjectChoice(self.part11, self.proj3, 3)
        participantProjectChoice(self.part11, self.proj4, 5)
        participantProjectChoice(self.part11, self.proj5, 5)
        participantProjectChoice(self.part11, self.proj6, 5)
        participantProjectChoice(self.part11, self.proj7, 2)
        participantProjectChoice(self.part11, self.proj8, 2)
        participantProjectChoice(self.part11, self.proj9, 2)
        participantProjectChoice(self.part11, self.proj10, 2)
        participantProjectChoice(self.part11, self.proj11, 1)
        participantProjectChoice(self.part11, self.proj12, 3)
        self.part12 = self.gf.addParticipant("Luke", "example@umbc5.edu")
        participantProjectChoice(self.part12, self.proj1, 2)
        participantProjectChoice(self.part12, self.proj2, 1)
        participantProjectChoice(self.part12, self.proj3, 3)
        participantProjectChoice(self.part12, self.proj4, 4)
        participantProjectChoice(self.part12, self.proj5, 4)
        participantProjectChoice(self.part12, self.proj6, 5)
        participantProjectChoice(self.part12, self.proj7, 5)
        participantProjectChoice(self.part12, self.proj8, 1)
        participantProjectChoice(self.part12, self.proj9, 1)
        participantProjectChoice(self.part12, self.proj10, 2)
        participantProjectChoice(self.part12, self.proj11, 2)
        participantProjectChoice(self.part12, self.proj12, 3)
        self.part13 = self.gf.addParticipant("Dona", "example@umbc.13edu")
        participantProjectChoice(self.part13, self.proj1, 5)
        participantProjectChoice(self.part13, self.proj2, 4)
        participantProjectChoice(self.part13, self.proj3, 5)
        participantProjectChoice(self.part13, self.proj4, 2)
        participantProjectChoice(self.part13, self.proj5, 3)
        participantProjectChoice(self.part13, self.proj6, 2)
        participantProjectChoice(self.part13, self.proj7, 1)
        participantProjectChoice(self.part13, self.proj8, 1)
        participantProjectChoice(self.part13, self.proj9, 1)
        participantProjectChoice(self.part13, self.proj10, 4)
        participantProjectChoice(self.part13, self.proj11, 3)
        participantProjectChoice(self.part13, self.proj12, 5)

        self.part14 = self.gf.addParticipant("Swaithi", "example@umbc14.edu")
        participantProjectChoice(self.part14, self.proj1, 2)
        participantProjectChoice(self.part14, self.proj2, 1)
        participantProjectChoice(self.part14, self.proj3, 3)
        participantProjectChoice(self.part14, self.proj4, 3)
        participantProjectChoice(self.part14, self.proj5, 1)
        participantProjectChoice(self.part14, self.proj6, 2)
        participantProjectChoice(self.part14, self.proj7, 5)
        participantProjectChoice(self.part14, self.proj8, 4)
        participantProjectChoice(self.part14, self.proj9, 3)
        participantProjectChoice(self.part14, self.proj10, 4)
        participantProjectChoice(self.part14, self.proj11, 4)
        participantProjectChoice(self.part14, self.proj12, 4)

        self.part15 = self.gf.addParticipant("Rhea", "example@um15bc.edu")
        participantProjectChoice(self.part15, self.proj1, 2)
        participantProjectChoice(self.part15, self.proj2, 3)
        participantProjectChoice(self.part15, self.proj3, 2)
        participantProjectChoice(self.part15, self.proj4, 1)
        participantProjectChoice(self.part15, self.proj5, 4)
        participantProjectChoice(self.part15, self.proj6, 5)
        participantProjectChoice(self.part15, self.proj7, 5)
        participantProjectChoice(self.part15, self.proj8, 5)
        participantProjectChoice(self.part15, self.proj9, 5)
        participantProjectChoice(self.part15, self.proj10, 2)
        participantProjectChoice(self.part15, self.proj11, 1)
        participantProjectChoice(self.part15, self.proj12, 3)
        self.part16 = self.gf.addParticipant("Rhiannon", "exampl16e@umbc.edu")
        participantProjectChoice(self.part16, self.proj1, 1)
        participantProjectChoice(self.part16, self.proj2, 1)
        participantProjectChoice(self.part16, self.proj3, 1)
        participantProjectChoice(self.part16, self.proj4, 1)
        participantProjectChoice(self.part16, self.proj5, 1)
        participantProjectChoice(self.part16, self.proj6, 2)
        participantProjectChoice(self.part16, self.proj7, 4)
        participantProjectChoice(self.part16, self.proj8, 5)
        participantProjectChoice(self.part16, self.proj9, 5)
        participantProjectChoice(self.part16, self.proj10, 1)
        participantProjectChoice(self.part16, self.proj11, 2)
        participantProjectChoice(self.part16, self.proj12, 4)
        self.part17 = self.gf.addParticipant("David", "example17@umbc.edu")
        participantProjectChoice(self.part17, self.proj1, 2)
        participantProjectChoice(self.part17, self.proj2, 4)
        participantProjectChoice(self.part17, self.proj3, 2)
        participantProjectChoice(self.part17, self.proj4, 4)
        participantProjectChoice(self.part17, self.proj5, 5)
        participantProjectChoice(self.part17, self.proj6, 5)
        participantProjectChoice(self.part17, self.proj7, 3)
        participantProjectChoice(self.part17, self.proj8, 5)
        participantProjectChoice(self.part17, self.proj9, 2)
        participantProjectChoice(self.part17, self.proj10, 3)
        participantProjectChoice(self.part17, self.proj11, 2)
        participantProjectChoice(self.part17, self.proj12, 5)

        self.part18 = self.gf.addParticipant("Jayce", "example18@umbc.edu")
        participantProjectChoice(self.part18, self.proj1, 2)
        participantProjectChoice(self.part18, self.proj2, 3)
        participantProjectChoice(self.part18, self.proj3, 2)
        participantProjectChoice(self.part18, self.proj4, 5)
        participantProjectChoice(self.part18, self.proj5, 4)
        participantProjectChoice(self.part18, self.proj6, 5)
        participantProjectChoice(self.part18, self.proj7, 3)
        participantProjectChoice(self.part18, self.proj8, 1)
        participantProjectChoice(self.part18, self.proj9, 2)
        participantProjectChoice(self.part18, self.proj10, 5)
        participantProjectChoice(self.part18, self.proj11, 5)
        participantProjectChoice(self.part18, self.proj12, 3)

        self.part19 = self.gf.addParticipant("JoJo", "example@um19bc.edu")
        participantProjectChoice(self.part19, self.proj1, 3)
        participantProjectChoice(self.part19, self.proj2, 3)
        participantProjectChoice(self.part19, self.proj3, 3)
        participantProjectChoice(self.part19, self.proj4, 4)
        participantProjectChoice(self.part19, self.proj5, 5)
        participantProjectChoice(self.part19, self.proj6, 4)
        participantProjectChoice(self.part19, self.proj7, 2)
        participantProjectChoice(self.part19, self.proj8, 3)
        participantProjectChoice(self.part19, self.proj9, 1)
        participantProjectChoice(self.part19, self.proj10, 2)
        participantProjectChoice(self.part19, self.proj11, 2)
        participantProjectChoice(self.part19, self.proj12, 3)
        self.part20 = self.gf.addParticipant("Mayor", "example@umb20c.edu")
        participantProjectChoice(self.part20, self.proj1, 5)
        participantProjectChoice(self.part20, self.proj2, 5)
        participantProjectChoice(self.part20, self.proj3, 5)
        participantProjectChoice(self.part20, self.proj4, 2)
        participantProjectChoice(self.part20, self.proj5, 3)
        participantProjectChoice(self.part20, self.proj6, 5)
        participantProjectChoice(self.part20, self.proj7, 1)
        participantProjectChoice(self.part20, self.proj8, 2)
        participantProjectChoice(self.part20, self.proj9, 3)
        participantProjectChoice(self.part20, self.proj10, 4)
        participantProjectChoice(self.part20, self.proj11, 4)
        participantProjectChoice(self.part20, self.proj12, 3)
        self.part21 = self.gf.addParticipant("Kristen", "ex21ample@umbc.edu")
        participantProjectChoice(self.part21, self.proj1, 1)
        participantProjectChoice(self.part21, self.proj2, 3)
        participantProjectChoice(self.part21, self.proj3, 5)
        participantProjectChoice(self.part21, self.proj4, 3)
        participantProjectChoice(self.part21, self.proj5, 2)
        participantProjectChoice(self.part21, self.proj6, 3)
        participantProjectChoice(self.part21, self.proj7, 3)
        participantProjectChoice(self.part21, self.proj8, 2)
        participantProjectChoice(self.part21, self.proj9, 3)
        participantProjectChoice(self.part21, self.proj10, 5)
        participantProjectChoice(self.part21, self.proj11, 2)
        participantProjectChoice(self.part21, self.proj12, 4)

        self.part22 = self.gf.addParticipant("Destiny", "exam22ple@umbc.edu")
        participantProjectChoice(self.part22, self.proj1, 1)
        participantProjectChoice(self.part22, self.proj2, 1)
        participantProjectChoice(self.part22, self.proj3, 1)
        participantProjectChoice(self.part22, self.proj4, 2)
        participantProjectChoice(self.part22, self.proj5, 3)
        participantProjectChoice(self.part22, self.proj6, 2)
        participantProjectChoice(self.part22, self.proj7, 4)
        participantProjectChoice(self.part22, self.proj8, 5)
        participantProjectChoice(self.part22, self.proj9, 4)
        participantProjectChoice(self.part22, self.proj10, 5)
        participantProjectChoice(self.part22, self.proj11, 4)
        participantProjectChoice(self.part22, self.proj12, 3)

        self.part23 = self.gf.addParticipant("Megan", "example@23umbc.edu")
        participantProjectChoice(self.part23, self.proj1, 3)
        participantProjectChoice(self.part23, self.proj2, 2)
        participantProjectChoice(self.part23, self.proj3, 3)
        participantProjectChoice(self.part23, self.proj4, 4)
        participantProjectChoice(self.part23, self.proj5, 4)
        participantProjectChoice(self.part23, self.proj6, 1)
        participantProjectChoice(self.part23, self.proj7, 5)
        participantProjectChoice(self.part23, self.proj8, 5)
        participantProjectChoice(self.part23, self.proj9, 5)
        participantProjectChoice(self.part23, self.proj10, 2)
        participantProjectChoice(self.part23, self.proj11, 3)
        participantProjectChoice(self.part23, self.proj12, 1)
        self.part24 = self.gf.addParticipant("Marzuq", "example@u24mbc.edu")
        participantProjectChoice(self.part24, self.proj1, 2)
        participantProjectChoice(self.part24, self.proj2, 4)
        participantProjectChoice(self.part24, self.proj3, 3)
        participantProjectChoice(self.part24, self.proj4, 3)
        participantProjectChoice(self.part24, self.proj5, 3)
        participantProjectChoice(self.part24, self.proj6, 1)
        participantProjectChoice(self.part24, self.proj7, 3)
        participantProjectChoice(self.part24, self.proj8, 5)
        participantProjectChoice(self.part24, self.proj9, 4)
        participantProjectChoice(self.part24, self.proj10, 2)
        participantProjectChoice(self.part24, self.proj11, 2)
        participantProjectChoice(self.part24, self.proj12, 1)
        self.part25 = self.gf.addParticipant("Baker", "example@umbc25.edu")
        participantProjectChoice(self.part25, self.proj1, 3)
        participantProjectChoice(self.part25, self.proj2, 4)
        participantProjectChoice(self.part25, self.proj3, 2)
        participantProjectChoice(self.part25, self.proj4, 2)
        participantProjectChoice(self.part25, self.proj5, 2)
        participantProjectChoice(self.part25, self.proj6, 2)
        participantProjectChoice(self.part25, self.proj7, 1)
        participantProjectChoice(self.part25, self.proj8, 5)
        participantProjectChoice(self.part25, self.proj9, 4)
        participantProjectChoice(self.part25, self.proj10, 5)
        participantProjectChoice(self.part25, self.proj11, 5)
        participantProjectChoice(self.part25, self.proj12, 5)
    
    def test_optimal_groupings(self):
        best_group, second_best, third_best = calc_optimal_groups(self.gf, 5, 100)

        print(best_group[1], second_best[1], third_best[1])
        self.assertGreater(best_group[1], second_best[1])
    
    def test_get_proj_score_after_initial_groupings(self):
        best_group, second_best, third_best = calc_optimal_groups(self.gf, 5, 100)
        #print(best_group)
        #print(get_individual_proj_scores(best_group[0], self.gf.getAttributeList()))
        self.assertEqual(get_individual_proj_scores(best_group[0], self.gf.getAttributeList()), best_group[1])
