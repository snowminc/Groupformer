"""Methods to determine the priority of a user to a group after answering
specific questions"""

from dbtools.models import Project, Participant, Attribute, attribute_selection
from django.db import models
import random

#calculate the priority for a group
def calc_project_priority(project, participant_list):
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
        val = 0
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

def calc_individual_priority(input_list):
    pass

# for this function, we need to handle keeping track of the minimum score
# in each of the projects and add to the master_score
def calc_global_score(project_list, participant_list):
    master_score = 0
    min_proj = 99999
    for project in project_list:
        val = calc_project_priority(project)
        if val < min_proj:
            min_proj = val
        master_score += val

    master_score += min_proj
    return master_score

def shuffle_particpants(group_former):
    roster = group_former.getRoster().copy()
    random.shuffle(roster)
    return roster

def calc_optimal_groups(gf, epoch=50, max_parts=4):
    """Uses random hill climbing algorithm to determine
    the "best" grouping of participants"""
    best_group_value = 0
    best_group_list = []
    #amount of people able to go into projects for evenness
    similar_group_number = len(gf.getProjectList()) / len(gf.getRoster())
    total_combinations = combinations_num(max_parts, len(gf.getRoster()))

    # do shuffle for amount of epochs or if we reached
    # the maximum total combinations possible
    for i in range(epoch) and i < total_combinations:
        roster = shuffle_particpants(gf)
        candidate_list = []
        while len(roster) > 0:
            temp_list = []
            for j in range(similar_group_number) and j < max_parts:
                candidate_list.append(roster.pop())
            candidate_list.append(temp_list.copy())

        temp = calc_global_score(gf.getProjectList(), candidate_list)

        if temp > best_group_value:
            for i in len(candidate_list):
                project = gf.getProjectList()[i]
                candidates = candidate_list[i]
                best_global_list.append(save_group(project, candidates))

    # returns a list of tupled project, with the participant roster
    return best_group_value

def save_group(project, candidate_list):
    return (project, candidate_list)

def combination_num(n, r):
    return factorial(n) / (factorial(r) * factorial(n-r))