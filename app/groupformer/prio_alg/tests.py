"""Testing participant, group, and response modules"""
from django.test import TestCase
from .models import *
from .group import Group
from .participant import Participant
from .response import Question


class PrioTest(TestCase):
    """Testing priority algorithm methods"""

    def test_participant(self):
        """Tests participant creation"""
        print("Testing participant module")
        part = Participant('User', 'user@email.com', 100)
        print(str(part))
        self.assertEquals("User", part.name)
        self.assertEquals("user@email.com", part.email)
        self.assertEquals(100, part.u_id)

    def test_roster(self):
        """Test adding participants to a roster"""
        print('Testing rosters\n')
        roster = []
        for x in range(5):
            roster.append(Participant(f"{x}", f"{x}@umbc.edu", x))
        for part in roster:
            print(str(part))

    def test_response(self):
        """Test question creation"""
        print('Testing Response\n')
        q = Question(0, "Would you like to work on proj1?", False)
        part = Participant('User', 'user@email.com', 100)
        submission = part.answer_question(q, 3)
        print(str(submission))

    def test_group(self):
        """Test group/project creation"""
        print("Testing groups\n")
        q = Question(0, "Would you like to work on proj1?", False)
        g = Group("proj1", q, "GroupFormer Tool", 0)
        print(str(g))

    def test_participant_answer_question(self):
        """Test participant answering a question"""

    def test_get_participants_score(self):
        """Test participant's score on several questions"""

    def test_get_group_score(self):
        """Test a group of participants getting scored"""

class GroupFormerTest(TestCase):
    """Testing database model with priority algorithm"""

    def test_get_participant(self):
        pass

    def test_get_roster(self):
        pass

    def test_get_project_list(self):
        pass

    def test_get_priority_for_participant(self):
        pass

    def test_get_group_score(self):
        pass

    def test_get_global_score(self):
        pass

    def test_shuffle_particpants(self):
        pass

    def test_optimal_particpant_score(self):
        pass

    def test_add_project_with_questions(self):
        pass
