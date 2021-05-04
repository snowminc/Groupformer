"""Methods to determine the priority of a user to a group after answering
specific questions"""

import random
import math
from dbtools.models import *

MAX_PRIO = 5
MIN_PRIO = 0
PERCENTAGE_THRESHOLD = .15


# calculate the priority for a group
def calc_project_priority(project, participant_list, attribute_list):
    """Calculates a projects priority.
    :param
        attribute_list (list) : is a list of attribute_selection
        participant_list (list) : is a list of Participant
        project (Project) : is of type Project

    :return
        value of score for a project and the list of participants given
    """
    # multi-step process
    # participant project attributes summed together
    # particpant attributes have the same id
    #   - Homogenous:
    #       -   get the rnge between the current value and
    #       -   the greatest outlier, then subtract
    #   - Hetergenous:
    #       -   get the rnge between the current value and
    #       -   the greatest outlier, then add
    tot_score = 0
    # get project score for each participant in the group
    for part in participant_list:
        try:
            tot_score += part.getProjectChoice(project).value

            if part.getDesiredPartnerList():
                # https://www.geeksforgeeks.org/python-check-if-one-list-is-subset-of-other/
                if all(x in participant_list for x in list(part.getDesiredPartnerList())):
                    tot_score += math.ceil((MAX_PRIO - MIN_PRIO) / 2)

        except (AttributeError):
            # give them an average score
            tot_score += 0

    if attribute_list != None:
        for att in attribute_list:
            # get the furthest rnge for each attribute among each participant and
            # add to the total score
            for i in range(len(participant_list)):
                part = participant_list[i]
                try:
                    part_val = participant_list[i].getAttributeChoice(att).value

                    # the idea here is to compare the value of the participant object with
                    # every one of the teammates and add/subtract based off of the rnge of
                    # that teammates score, use a for loop to only count the iterations
                    # past the indexed participant
                    # we don't want to account for a teammates comparison twice
                    for j in range(i, len(participant_list)):
                        teammate = participant_list[j]
                        if teammate is not part:
                            try:
                                teammate_val = teammate.getAttributeChoice(att).value
                                rnge = abs(teammate_val - part_val)

                                if att.is_homogenous:
                                    rnge = rnge * -1

                                tot_score += rnge
                            # participant didn't enter data for an attribute
                            # so just skip it
                            except (AttributeError):
                                continue
                except (AttributeError):
                    # if there is no value for an attribute
                    continue

    return tot_score


def greater_difference(min_num, val, max_num):
    """returns the greater difference between a value
    and two numbers

    :param
        min_num (int) : a number to check
        val (int) : the number to compare to other params
        max_num (int) : a number to check
    :return
        absolute value of greatest difference between two compared numbers"""
    if abs(max_num - val) > abs(min_num - val):
        return abs(max_num - val)
    else:
        return abs(min_num - val)


# for this function, we need to handle keeping track of the minimum score
# in each of the projects and add to the master_score
def calc_global_score(project_candidate_list, attribute_list):
    """Calculates the global score of a parsed out group of projects and candidates
    Use function: create_random_candidate_groups

    :param
         project_candidate_list (list of tuples) : Information about a list of
         grouped projects and their potential candidates. Overall list structure:

         [
            (project, [candidates]),
            (project, [candidates]),
            ...
         ]
         attribute_list (queryset or list) : list of Attribute objects that may or may
         not be answered by participants

    """
    master_score = 0
    min_proj = 99999
    for i in range(len(project_candidate_list)):
        val = calc_project_priority(project_candidate_list[i][0], project_candidate_list[i][1], attribute_list)
        # check if the project has a candidate list associated,
        # if it doesn't, it doesn't get counted for the min_proj score
        if val < min_proj and len(project_candidate_list[i][1]) != 0:
            min_proj = val
        master_score += val

    master_score += min_proj
    return master_score


def shuffle_list(ref_list):
    """Utility function to return the copy of a shuffled list.
    NOTE: If more than one element resides in list, it will ensure the
    returned copy isn't the same as the referenced list

    :param
        ref_list (list) : a generic list

    :return
        a shuffled deep copy of the ref_list"""
    shuf_list = ref_list.copy()

    if len(ref_list) > 1:
        while check_if_exactly_equal(shuf_list, ref_list):
            random.shuffle(shuf_list)

    return shuf_list


def calc_optimal_groups(gf, max_parts=4, epoch=0):
    """Uses random hill climbing algorithm to determine
    the "best" grouping of participants

    :param
        gf (groupformer) : groupformer instance

        max_parts (int) : maximum participants allowed per group

        epoch (int) : iterations to search for an optimal group (higher values will
        generally lead to higher accuracy)

    :return
        (best_group, val), (second_best, val), (third_best, val) : (groups,val) tuple where
        groups is [(project,participant_list), ...] where each candidate_list has participants
        to match to the project and val is the master priority of all of the groups in groups list
        returns top three groupings in tuples (group, value)"""
    if epoch == 0:
        epoch = combination_num(max_parts, len(gf.getProjectList()))
    
    best_group_value = 0
    best_group_list = []
    second_best_value = 0
    second_best_group_list = []
    third_best_value = 0
    third_best_group_list = []
    # amount of people able to go into projects for evenness
    # total_combinations = combination_num(max_parts, len(gf.getRoster()))

    # do shuffle for amount of epochs or if we reached
    # the maximum total combinations possible
    for i in range(epoch):
        # if i >= total_combinations:
        # break
        group_list = create_random_candidate_groups(gf, max_parts)

        temp = calc_global_score(group_list, gf.getAttributeList())
        # print(temp)
        if temp >= best_group_value:
            best_group_list = group_list.copy()
            best_group_value = temp
        elif temp >= second_best_value:
            second_best_group_list = group_list.copy()
            second_best_value = temp
        elif temp >= third_best_value:
            third_best_group_list = group_list.copy()
            third_best_value = temp

    # returns a list of tupled project, with the participant roster
    return (best_group_list, best_group_value), (second_best_group_list, second_best_value), (
    third_best_group_list, third_best_value)


def save_group(project, candidate_list):
    """Groups project and the proj's candidate list into a tuple
    :param
        project(Project) : a project
        candidate_list (participants) : list of participant objects

    :return
        tupled object of type (project, [Participant])"""
    return (project, candidate_list)


def combination_num(n, r):
    """Combination formula to calculate the maximum amount of different combinations
    "n choose r"
    :param
        n (int) : n distict objects
        r (int) : sample of r elements

    :return
        Returns result of combination calculation"""
    if n < r:
        raise Exception()('n cannot be less than r')
    if n == 0 or r == 0:
        raise Exception('n or r cannot be 0')
    return math.factorial(n) / (math.factorial(r) * math.factorial(n - r))


def create_random_candidate_groups(gf, max_parts):
    """creates a random candidate list from list of lists and maps to projects
    tuple structure (project, [candidates]).

    :param
        gf (groupformer) : instance of a groupformer object to pull participant
                        and project data from
        max_parts (int) : maximum participants allowed per group.
                NOTE: If there are more people than allowable projects, then the participant limit
                may be exceeded to ensure total particpation of a group formers roster

    :return
        group_list (list with tuple of project and a list) :
        Overall list structure:
            [
            (project, [candidates]),
            (project, [candidates]),
            ...
            ]
    """
    project_list = shuffle_list(list(gf.getProjectList()))
    roster = shuffle_list(list(gf.getRoster()))
    even_members_per_group = math.ceil(len(roster) / float(max_parts))
    # lists of lists of candidates
    candidate_lists = []
    # print(even_members_per_group)
    # do we want even distribution or do we want to prioritize better
    # creates lists of max_part or optimal sized groups
    # evenly spreads out participants and ensures all projects have someone
    # assigned to them. may want to prioritze better groupings rather than
    # assigning every project

    # case where every project gets max participants
    if len(project_list) == even_members_per_group:
        while len(roster) > 0:
            temp_list = []
            # pop the roster onto the temp list for the
            # amount of max_participants
            for j in range(max_parts):
                if j >= max_parts:
                    break
                elif len(roster) == 0:
                    break
                else:
                    temp_list.append(roster.pop())

            candidate_lists.append(temp_list.copy())

    # case where we have more people than allowable participants
    elif len(project_list) < even_members_per_group:
        # normally fill up the lists, then add equally to each subsequent
        # proj until we finish the pushing to roster
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

            # when the project list count meets candidate list
            if len(project_list) == len(candidate_lists):
                for j in range(roster):
                    candidate_lists[j % len(project_list)].append(roster.pop())

    # case where projects will have 0 or more people
    # all projects aren't full
    elif len(project_list) > even_members_per_group:
        # put random people into random groups and bias towards
        # groups with more people than groups with just one person
        # initialize the candidate_list with projects
        for i in range(len(project_list)):
            candidate_lists.append([])

        j = 0
        while len(roster) > 0:
            # print(roster)
            # get random amount of people to be partnered up from 0 to max_participants
            # if roster length remaining is larger than the max participants
            # get a random number between 0 and the max_participants
            # else the roster length remaining is smaller than the max allowable participants
            # get a random number between 0 and the range of the length of the roster

            # only step into this if we can put people into a bucket
            if len(candidate_lists[j]) < max_parts:

                # get a random number between 0 and the maximum participants to a group
                num_parts = random.randint(0, max_parts)

                # check if the addition of the participants would exceed the max_participant
                # limit, if it does then get the remaining available spots and fill them
                # with participants
                if num_parts + len(candidate_lists[j]) > max_parts:
                    num_parts -= len(candidate_lists[j])

                # print(num_parts)
                for i in range(num_parts):
                    if len(roster) == 0:
                        break
                    else:
                        candidate_lists[j].append(roster.pop())

            # make sure j mods the list size so we don't iterate passed the list
            # print(candidate_lists)
            # have to decrement the size becuase we do the operation THEN check,
            # not check then iterate
            if j < len(candidate_lists) - 1:
                j += 1
            else:
                j = 0

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


# returns the group score in a list of tuples
def get_individual_proj_scores(group_list, attribute_list):
    """ Description: Get scores and packages them with their corresponding
        project

        Note: should use calc_optimal_groups and subscript the result
        with result[0]

        :param
            group_list (list of tuples) : each element is a tuple that contains
                                        a (project, [participant_list]) where project
                                        is of type project and participant list is of
                                        type participant
        :return
            proj_list (list of tuple with project(project), and priority(float)
            [(project, proj_score), ...] : Returns a list of with tuples of a project
                and the projects respective score.
        """
    proj_list = []
    for group_tuple in group_list:
        proj_name = group_tuple[0]
        proj_parts = group_tuple[1]
        proj_prio = calc_project_priority(proj_name, proj_parts, attribute_list)
        proj_list.append((proj_name, proj_prio))
    return proj_list


def check_if_exactly_equal(list_1, list_2):
    """
    Referenced and pulled from:
    https://thispointer.com/python-check-if-two-lists-are-equal-or-not-covers-both-ordered-unordered-lists/
    Checks if two lists are exactly identical

    :param
        list_1 (list): generic list
        list_2 (list): generic list
    :return
        bool : tells if lists are similar or not
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
