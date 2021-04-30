"""Methods to determine the priority of a user to a group after answering
specific questions"""

import random
import math
from dbtools.models import *

MAX_PRIO = 5
MIN_PRIO = 0
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
        try:
            tot_score += part.getProjectChoice(project).value

            if part.desired_partner != None:
                if part.desired_partner in list(participant_list):
                    tot_score += math.ceil((MAX_PRIO-MIN_PRIO)/2)

        except (AttributeError):
            #give them an average score
            tot_score += math.ceil(MAX_PRIO+MIN_PRIO/2)

    for att in attribute_list:
        # to get the outliers of the answers
        max_num = MIN_PRIO
        min_num = MAX_PRIO
        val = 0
        #find if we need to change the max/min values
        for part in participant_list:
            try:
                val = part.getAttributeChoice(att).value
                if val < min_num:
                    min_num = val
                if val > max_num:
                    max_num = val
            except (AttributeError): #if the user didn't answer a question
                val = 0
            
        
        #get the furthest range for each attribute among each participant and 
        #add to the total score
        for part in participant_list:

            try:
                val = part.getAttributeChoice(att).value

                if abs(max_num-val) > abs(min_num-val):
                    val = abs(max_num-val)
                else:
                    val = abs(min_num-val)

                if att.attribute.is_homogenous:
                    val = val * -1
            except (AttributeError):
                val = 0

            tot_score += val
        
        return tot_score
def calc_individual_priority(input_list):
    pass

def update_min_prio(x):
    MIN_PRIO = x

def update_max_prio(x):
    MAX_PRIO = x

# for this function, we need to handle keeping track of the minimum score
# in each of the projects and add to the master_score
def calc_global_score(project_candidate_list, attribute_list):
    """Calculates the global score of a parsed out group of projects and candidates
    Use function: create_random_candidate_groups
    Overall list structure:
        [
            (project, [candidates]),
            (project, [candidates]),
            ...
        ]
    """
    master_score = 0
    min_proj = 99999
    for i in range(len(project_candidate_list)):
        val = calc_project_priority(project_candidate_list[i][0], project_candidate_list[i][1], attribute_list)
        #check if the project has a candidate list associated,
        #if it doesn't, it doesn't get counted for the min_proj score
        if val < min_proj and len(project_candidate_list[i][1]) != 0:
            min_proj = val
        master_score += val

    master_score += min_proj
    return master_score

def shuffle_list(ref_list):
    """Utility function to return the copy of a shuffled list.
    NOTE: If more than one element resides in list, it will ensure the
    returned copy isn't the same as the referenced list"""
    shuf_list = ref_list.copy()

    if len(ref_list) > 1:
        while check_if_exactly_equal(shuf_list, ref_list):
            random.shuffle(shuf_list)

    return shuf_list

def calc_optimal_groups(gf, max_parts=4, epoch=50):
    """Uses random hill climbing algorithm to determine
    the "best" grouping of participants"""
    best_group_value = 0
    best_group_list = []
    #amount of people able to go into projects for evenness
    #total_combinations = combination_num(max_parts, len(gf.getRoster()))

    # do shuffle for amount of epochs or if we reached
    # the maximum total combinations possible
    for i in range(epoch):
        #if i >= total_combinations:
            #break
        group_list = create_random_candidate_groups(gf, max_parts)

        temp = calc_global_score(group_list, gf.getAttributeList())

        if temp > best_group_value:
            best_group_list = group_list.copy()
            best_group_value = temp

    # returns a list of tupled project, with the participant roster
    return best_group_list

def save_group(project, candidate_list):
    """Groups project and the proj's candidate list into a tuple"""
    return (project, candidate_list)

def combination_num(n, r):
    """Combination formula"""
    return math.factorial(n) / (math.factorial(r) * math.factorial(n-r))

def create_random_candidate_groups(gf, max_parts):
    """creates a random candidate list from list of lists and maps to projects
    tuple structure (project, [candidates]).
    
    Overall list structure:
        [
            (project, [candidates]),
            (project, [candidates]),
            ...
        ]
    """
    project_list = shuffle_list(list(gf.getProjectList()))
    roster = shuffle_list(list(gf.getRoster()))
    even_members_per_group = math.ceil(len(roster)/float(max_parts))
        #lists of lists of candidates
    candidate_lists = []

    #do we want even distribution or do we want to prioritize better
    #creates lists of max_part or optimal sized groups
    #evenly spreads out participants and ensures all projects have someone
    #assigned to them. may want to prioritze better groupings rather than
    #assigning every project

    #case where every project gets max participants
    if len(project_list) == even_members_per_group:
        while len(roster) > 0:
            temp_list = []
            for j in range(max_parts):
                if j >= max_parts:
                    break
                elif len(roster) == 0:
                    break
                else:
                    temp_list.append(roster.pop())
        candidate_lists.append(temp_list.copy())

    #case where we have more people than allowable participants
    elif len(project_list) < even_members_per_group:
        #normally fill up the lists, then add equally to each subsequent
        #proj until we finish the pushing to roster
        while len(roster) > 0:
            temp_list = []
            for j in range(max_parts):
                if j >= max_parts:
                    break
                elif len(roster) == 0:
                    break
                else:
                    temp_list.append(roster.pop())
            candidate_lists.append(temp_list.copy())

            #when the project list count meets candidate list
            if len(project_list) == len(candidate_lists):
                for j in range(roster):
                    candidate_lists[j%len(project_list)].append(roster.pop())

    #case where projects will have 0 or more people
    #all projects aren't full
    elif len(project_list) > even_members_per_group:
        #put random people into random groups and bias towards
        #groups with more people than groups with just one person
        #initialize the candidate_list with projects
        for i in range(len(project_list)):
            candidate_lists.append([])
        
        j = 0
        while len(roster) > 0:
            
            #get random amount of people to be partnered up from 0 to max_participants
            #if roster length remaining is larger than the max participants
            #get a random number between 0 and the max_participants
            #else the roster length remaining is smaller than the max allowable participants
            #get a random number between 0 and the rang of the length of the roster
            if max_parts <= len(roster):
                num_parts = random.randint(0, max_parts)
            else:
                num_parts = random.randint(0, len(roster))
            temp_list = []
            for i in range(num_parts):
                if len(roster) == 0:
                    break
                else:
                    temp_list.append(roster.pop())
            
            #we should never get to the point where we infinite loop because the random int is
            # bound to the limits of the roster length, we just have to search the buckets that
            # can fit the remaining participants 
            while len(temp_list) + len(candidate_lists[j%len(candidate_lists)-1]) > max_parts:
                j += 1
            #make sure j mods the list size so we don't iterate passed the list
            candidate_lists[j%len(candidate_lists)-1].append(temp_list)
            j += 1
            

     
    # combine the projects with their respective candidate lists
    group_list = []
    # make sure that there aren't more candidate lists than there are projects
    if len(candidate_lists) > len(project_list):
        raise Exception('Candidate list length is longer than project list length')

    total = len(candidate_lists)
    for i in range(total):
            project = project_list[i]
            candidates = candidate_lists[i]
            group_list.append(save_group(project, candidates))
    
    return group_list

def check_if_exactly_equal(list_1, list_2):
    """ 
    Referenced and pulled from:
    https://thispointer.com/python-check-if-two-lists-are-equal-or-not-covers-both-ordered-unordered-lists/
    Checks if two lists are exactly identical
    """
    # check if both the lists are of same size
    if len(list_1) != len(list_2):
        return False
    # create a zipped object from 2lists
    final_list = zip(list_1, list_2)
    # iterate over the zipped object
    for elem in final_list:
        if elem[0] != elem[1]:
            return False
    return True
