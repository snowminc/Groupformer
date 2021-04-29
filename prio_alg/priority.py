"""Methods to determine the priority of a user to a group after answering
specific questions"""

from .models import Project, Participant, Attribute, attribute_selection
from django.db import models
import random

#calculate the priority for a group
def calc_project_priority(project):
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

def calc_project_priority(input_list):
    """Calculates a projects priority.
    @Params: input is a list of lists of tuples
        group list of participants - jim, jean, joe
        secondary list is their responses - jim - list of tupled responses
                                            jean - list of tupled responses
                                            joe - list of tupled responses
    list of tuples
    (ans_id, priority_number, true if attribute or false if proj, boolean of homogenous or heterogenous)"""
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
    #make loops more readable
    ans_id = 0
    prio = 1
    proj = 2
    homogenous = 3

    # get project score for each participant in the group
    for particpant in input_list:
        for i in particpant:
            if i[proj] == True:
                tot_score += i[prio]
            elif i[proj] == False:
                if i[homogenous] == True:
                    
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

# for this function, we need to handle keeping track of the minimum score
# in each of the projects and add to the master_score
def calc_global_score(project_list):
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
    for i in range(epoch):
        roster = shuffle_particpants(gf)
        candidate_list = []
        for j in range(max_parts):
            candidate_list.append(roster.pop())
    #
    return best_group_value, best_group
