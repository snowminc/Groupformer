class Question:
    """Has values about a question and has flags denoting
    how it should be compared among other questions. 
    (i.e. Should be paired with like answers or unlike answers)"""
    max_scale = 5
    min_scale = 0
    def __init__(self, q_id, question, attribute=False, homogenous=True):
        self.question = question
        self.attribute = attribute
        self.homogenous = homogenous
        self.q_id = q_id

    def __str__(self):
        """returns the question in a string format"""
        return f"ID: {self.q_id} \nQuestion: {self.question}"\
               + f"\nHomogeneity={self.homogenous}\n"
    

class Answer:
    """Has values about an answer to a question and also can contain
    other information, such as desired partners, answer scale, yes/no"""
    def __init__(self, ans, a_id):
        self.answer = ans
        self.a_id = a_id

    def __str__(self):
        return f"{str(self.a_id)}: {str(self.answer)}"

    def get_ans(self):
        return f"ID: {self.a_id}\nAnswer: {self.answer}"


class YesNo(Answer):
    """Type determination for a yes/no answer to a question"""
    def __init__(self, ans, a_id):
        if str(ans).lower == 'yes':
            self.answer = self.max_scale
        elif str(ans).lower == 'no':
            self.answer = self.min_scale
        else:
            raise Exception('Invalid yes or no answer')
        self.a_id = a_id


class Scale(Answer):
    """Type determination for a scaled answer to a question"""


class Response:
    """Holds data about a users question and their answer"""
    def __init__(self, ans, ques, user):
        self.answer = ans
        self.ques = ques
        self.user = user

    def __str__(self):
        return f"Answer: {str(self.ques)}{str(self.answer)}\n{str(self.user)}"
