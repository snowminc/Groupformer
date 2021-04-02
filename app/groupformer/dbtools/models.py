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
        return self.prof_name + ' : ' + self.class_section 
    
    """
        Wrappers of the helper functions at the bottom of the file
        for extra ease of use and OO design
    """
    
    def addAttribute(self, name, is_homogenous, is_continuous):
        return addAttribute(self, name, is_homogenous, is_continuous)
    
    def addProject(self, name, description):
        return addProject(self,name,description)
    
    def addParticipant(self, name, email):
        return addParticipant(self, name, email)

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
    
    """
        Wrappers of the relationship helper functions
        for ease of use and more OO design
    """
    
    def attributeChoice(self, attribute, value):
        return participantAttributeChoice(self,attribute,value)
    
    def projectChoice(self, project, value):
        return participantProjectChoice(self,project,value)
    
    def desires(self, p):
        participantDesiredPartner(self,p)

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
    p = GroupFormer.objects.create(prof_name=name,
                                   prof_email=email,
                                   class_section=section)
    p.save()
    return p

def addAttribute(gf, name, is_homogenous, is_continuous):
    p = Attribute.objects.create(group_former=gf,
                                 attr_name=name,
                                 is_homogenous=is_homogenous,
                                 is_continuous=is_continuous)
    p.save()
    return p

def addProject(gf, name, description):
    p = Project.objects.create(group_former=gf,
                               project_name=name,
                               project_description=description)
    p.save()
    return p

def addParticipant(gf, name, email):
    p = Participant.objects.create(group_former=gf,
                                   part_name=name,
                                   part_email=email)
    p.save()
    return p

"""
    Each of the following adds an instance of the relationships
    They take in the attributes required of that relationship,
    add it to the database, and return on object of the relationship
"""

def participantAttributeChoice(participant,attribute,value):
    # Required checks - that they both are in the same GroupFormer
    # and that if the Attribute is discrete, it contains an integer value
    if participant.group_former != attribute.group_former:
        raise ValueError(str(participant)+" and "+str(attribute)+" are not part of the same GroupFormer")
    if not attribute.is_continuous:
        if value != int(value):
            raise ValueError('value of '+str(attribute)+' must be discrete')
    
    p = attribute_selection.objects.create(participant=participant,
                                           attribute=attribute,
                                           value=value)
    
    p.save();
    return p

def participantProjectChoice(participant,project,value):
    # Required that both participant and project be in the same GroupFormer
    if participant.group_former != project.group_former:
        raise ValueError(str(participant)+" and "+str(project)+" are not part of the same GroupFormer")
    
    p = project_selection.objects.create(participant=participant,
                                         project=project,
                                         value=value)
    
    p.save()
    return p

"""
    Adds an instance of the desired partner relation
    :param wanter: the Participant who wishes to work with the wantee
    :param wantee: the Participant who is wished to be worked with
    :return: Nothing, as the relationship is internal to the Participant model
"""
def participantDesiredPartner(wanter,wantee):
    #Required that both participants are in the same GroupFormer
    if wanter.group_former != wantee.group_former:
        raise ValueError(str(wanter)+" and "+str(wantee)+" are not part of the same GroupFormer")
    
    wanter.desired_partner.add(wantee)