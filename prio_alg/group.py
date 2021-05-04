"""Describes a group or project that the creator of the groupformer
wants to define"""
import random


class Group:
    """A group denotes a project that contains a list of
    people that are in the project. The project has a priority
    queue that determines the priority of students that are interested
    in participating in the project"""
    # roster = []
    min_participants = 0
    max_participants = 0

    def __init__(self, g_id, title, question, description):
        # sorted list to hold candidates
        self.candidate_list = []
        self.title = title
        self.question = question
        self.description = description
        self.score = 0
        self.g_id = g_id

    def __str__(self):
        return f"{self.g_id}, {self.title}, {self.description}"

    def set_min_participants(self, min_part):
        """Sets the minimum allowable participants"""
        self.min_participants = min_part

    def set_max_participants(self, max_part):
        """Sets the max allowable participants"""
        self.max_participants = max_part

    def get_local_score(self):
        """Sums the score of every candidate"""
        for candidate in self.candidate_list:
            self.score += candidate.get_score()
    # def set_roster(user_list)
    #    roster = user_list


    def set_candidate(self, roster):
        """This method is where a project will randomly pull a
        participant from the roster"""
        if len(self.candidate_list) < self.max_participants and len(roster) > 0:
            random.shuffle(roster)
            participant = roster.pop()
            self.candidate_list.append(participant)

    def get_candidate_list(self):
        """Gets candidate list for a group"""
        return self.candidate_list
