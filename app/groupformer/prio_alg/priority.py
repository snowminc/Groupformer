"""Methods to determine the priority of a user to a group after answering
specific questions"""

from .models import Project, Participant, Attribute, attribute_selection
from django.db import models

#calculate the priority for a group
def calc_project_priority(project, participant_list, attribute_list):
    """Calculates a projects priority.
    @Params: attribute_list is a list of attribute_selection
             participant_list is a list of Participant
             project is of type Project"""
    # multi-step process
    # participant project attributes summed together
    # particpant attributes have the same id
    #   - Homogenous:
    #       -   get the range between the current value and
    #       -   the greatest outlier, then subtract
    #   - Hetergenous:
    #       -   get the range between the current value and
    #       -   the greatest outlier, then add
    tot_score = 0

    # get project score for each participant in the group
    for part in participant_list:
        tot_score += part.getProjectChoice(project)

    for att in attribute_list:
        # to get the outliers of the answers
        max_num = 0
        min_num = 5
        #find if we need to change the max/min values
        for part in participant_list:
            val = part.getAttributeChoice(att).value
            if val < min_num:
                min_num = val
            if val > max_num:
                max_num = val
        
        #get the furthest range for each attribute among each participant and 
        #add to the total score
        for part in participant_list:
            val = part.getAttributeChoice(att).value

            if abs(max_num-val) > abs(min_num-val):
                val = abs(max_num-val)
            else:
                val = abs(min_num-val)

            if att.attribute.is_homogenous:
                val = val * -1

            tot_score += val
        
        return tot_score

def calc_global_score(group_former):
    roster = group_former.getRoster().copy()
    for projects in Project.objects.all():
        
        

def calc_optimal_groups(gf, epoch=50):
    pass

def get_random_participant_list(roster, max_count):
    """This method is where a project will randomly pull a
        participant from the roster"""
        candidatelist = []
        for i in range(max_count) and len(roster) > 0:
            random.shuffle(roster)
            participant = roster.pop()
            candidate_list.append(participant)

        return candidate_list
