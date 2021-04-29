"""Testing participant, group, and response modules"""
from django.test import TestCase
from dbtools.models import *
from .priority import *

# class PrioTest(TestCase):
#     """Testing priority algorithm methods"""

#     def test_participant(self):
#         """Tests participant creation"""
#         print("Testing participant module")
#         part = Participant('User', 'user@email.com', 100)
#         print(str(part))
#         self.assertEquals("User", part.name)
#         self.assertEquals("user@email.com", part.email)
#         self.assertEquals(100, part.u_id)

#     def test_roster(self):
#         """Test adding participants to a roster"""
#         print('Testing rosters\n')
#         roster = []
#         for x in range(5):
#             roster.append(Participant(f"{x}", f"{x}@umbc.edu", x))
#         for part in roster:
#             print(str(part))

#     def test_response(self):
#         """Test question creation"""
#         print('Testing Response\n')
#         q = Question(0, "Would you like to work on proj1?", False)
#         part = Participant('User', 'user@email.com', 100)
#         submission = part.answer_question(q, 3)
#         print(str(submission))

#     def test_group(self):
#         """Test group/project creation"""
#         print("Testing groups\n")
#         q = Question(0, "Would you like to work on proj1?", False)
#         g = Group("proj1", q, "GroupFormer Tool", 0)
#         print(str(g))

#     def test_participant_answer_question(self):
#         """Test participant answering a question"""

#     def test_get_participants_score(self):
#         """Test participant's score on several questions"""

#     def test_get_group_score(self):
#         """Test a group of participants getting scored"""

class GroupFormerTest(TestCase):
    """Testing database model with priority algorithm"""

    def setUp(self):
        print("Adding database elements manually (.objects.create())")
        self.gf = addGroupFormer("Petra", "pnadir@umbc.edu", "Grass watching")
        attr = self.gf.addAttribute("A", True, False)
        self.gf.addAttribute("Like salad", True, False)
        self.gf.addAttribute("Backend dev", False, False)
        proj2 = addProject(self.gf, "On top of the hill",
                           "This grass needs to be watched")
        self.gf.addParticipant("Joe", "JoeShmoe@aol.com")
        self.gf.addParticipant("BigDog", "bigdogsgottaeat@food.com")

    #answer the questions
        self.gf.getParticipantByName("Joe").attributeChoice(
            self.gf.getAttribute("Like salad"), 1)
        self.gf.getParticipantByName("BigDog").attributeChoice(
            self.gf.getAttribute("Like salad"), 5)
        self.gf.getParticipantByName("Joe").attributeChoice(
            self.gf.getAttribute("Backend dev"), 3)
        self.gf.getParticipantByName("BigDog").attributeChoice(
            self.gf.getAttribute("Backend dev"), 4)

    def test_get_groupformer(self):
        print(str(self.gf))
    
    def test_get_participant(self):
        part = self.gf.getParticipantByName("BigDog")
        print(str(part))

    def test_get_roster(self):
        roster = getGroupFormer("Petra", "Grass watching").getRoster()
        print(str(roster))

    def test_get_project_list(self):
        project_list = getGroupFormer("Petra", "Grass watching").getProjectList()
        print(str(project_list))

    def test_get_priority_for_participant_for_project(self):
        pass

    def test_get_group_score(self):
        project = getGroupFormer("Petra", "Grass watching").getProject("On top of the hill")
        #print(str(calc_project_priority()))
        pass

    def test_get_global_score(self):
        pass

    def test_shuffle_particpants(self):
        pass

    def test_optimal_particpant_score(self):
        pass

    def test_add_project_with_questions(self):
        pass

    def test_get_project_score(self):
        
        pass
