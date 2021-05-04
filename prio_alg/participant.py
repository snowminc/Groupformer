"""Particpant Module to describe particpant of a roster/list"""
from .response import Response
from .response import Answer


class Participant:
    """Participant class describes a participant of a roster/class"""
    def __init__(self, name, email, u_id):
        self.name = name
        self.email = email
        self.u_id = u_id
        self.response_list = []
        self.score = 0
        self.group = None

    def set_response_list(self, r_list):
        """Sets the response list"""
        self.response_list = r_list

    def set_group(self, group):
        self.group = group

    def get_score(self):
        """Retrieves the score from the responses"""
        for response in self.response_list:
            self.score += response.get_score

    def answer_question(self, ques, ans):
        """Answer a question and give it a score"""
        res = Response(Answer(ans, len(self.response_list)), ques, self)
        self.response_list.append(res)
        return res

    def __str__(self):
        return f"{self.u_id}, {self.name}, {self.email}, {str(self.group)}"
