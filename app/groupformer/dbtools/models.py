from django.db import models

# Use 
# from dbtools.models import *
# To import database models, functions

#Entities

# See the E-R diagram

class GroupFormer(models.Model):
    prof_name = models.CharField(max_length=200)
    prof_email = models.CharField(max_length=200)
    class_section = models.CharField(max_length=100)
    
    def __str__(self):
        return self.prof_name + ' ' + self.class_section 

class Project(models.Model):
    # Required to test relation involving it
    # To be replaced by Sarah's
    group_former = models.ForeignKey(GroupFormer, on_delete = models.CASCADE)
    project_name = models.CharField(max_length=200)
    project_description = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.project_name + ' (' + str(self.group_former) + ')'

class Attribute(models.Model):
    group_former = models.ForeignKey(GroupFormer, on_delete = models.CASCADE)
    attr_name = models.CharField(max_length=100)
    is_homogenous = models.BooleanField()
    is_continuous = models.BooleanField()
    
    def __str__(self):
        return self.attr_name + ' (' + str(self.group_former) + ')'
    

class Participant(models.Model):
    group_former = models.ForeignKey(GroupFormer, on_delete = models.CASCADE)
    part_name = models.CharField(max_length=200)
    part_email = models.CharField(max_length=200)
    
    desired_partner = models.ManyToManyField('self',blank=True,symmetrical=False)
    attributes = models.ManyToManyField(Attribute,through='attribute_selection')
    projects = models.ManyToManyField(Project,through='project_selection')
    
    def __str__(self):
        return self.part_name + ' (' + str(self.group_former) + ')'

# Relationships

class attribute_selection(models.Model):
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete = models.CASCADE)
    value = models.IntegerField()
    
    def __str__(self):
        return str(self.participant) + '-' + str(self.attribute)

class project_selection(models.Model):
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    value = models.FloatField()
    def __str__(self):
        return str(self.participant) + '-' + str(self.project)

# Helper functions

def addRoster(gf, roster):
    """
        Adds an entire roster to the Participants of a GroupFormer
       :param roster: In the form [[name : email] ...]
       :return: an array of Participant that were added
    """
    ps = []
    for (name,email) in roster:
        ps = ps + [addParticipant(gf.pk,name,email)]
    return ps

""" 
    Each of the following takes the required attributes
    Of their associated model, and returns an instance of that model
    after adding it to the database
"""

def addGroupFormer(name,email,section):
    p = GroupFormer(name, email, section)
    p.save()
    return p

def addAttribute(gf, name, is_homogenous, is_continuous):
    p = Attribute(gf.pk, name, is_homogenous, is_continuous)
    p.save()
    return p

def addProject(gf, name, description):
    p = Project(gf.pk, name, description)
    p.save()
    return p

def addParticipant(gf, name, email):
    p = Participant(gf.pk,name,email)
    p.save()
    return p

def participantAttributeChoice(participant,attribute,value):
    # Required checks - that they both are in the same GroupFormer
    # and that if the Attribute is discrete, it contains an integer value
    if participant.group_former != attribute.group_former:
        raise ValueError(str(participant)+" and "+str(attribute)+" are not part of the same GroupFormer")
    if not attribute.is_continuous:
        if value != int(value):
            raise ValueError('value of '+str(attribute)+' must be discrete')
    p = attribute_selection(participant,attribute,value)
    p.save();
    return p

def participantProjectChoice(participant,project,value):
    # Required that both participant and project be in the same GroupFormer
    if participant.group_former != project.group_former:
        raise ValueError(str(participant)+" and "+str(project)+" are not part of the same GroupFormer")
    p = project_selection(participant,project,value)
    p.save()
    return p
