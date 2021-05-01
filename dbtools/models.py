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
    
    def addRoster(self, roster):
        return addRoster(self, roster)
    
    """
        Getters of different parts of the GroupFormer
        :param name: the corresponding name
        :return: Either the corresponding project, attribute, or participant, or None
        :error: TypeError if there are more than one corresponding model
    """
    
    def getProject(self, name):
        recieved = Project.objects.filter(group_former=self,project_name=name)
        if len(recieved) > 1:
            raise ValueError('There are more than one '+name+' in '+str(self))
        if len(recieved) == 1:
            return recieved[0]
        else:
            return None
    
    def getAttribute(self, name):
        recieved = Attribute.objects.filter(group_former=self,attr_name=name)
        if len(recieved) > 1:
            raise ValueError('There are more than one '+name+' in '+str(self))
        if len(recieved) == 1:
            return recieved[0]
        else:
            return None
    
    def getParticipantByName(self, name):
        recieved = Participant.objects.filter(group_former=self,part_name=name)
        if len(recieved) > 1:
            raise ValueError('There are more than one '+name+' in '+str(self))
        if len(recieved) == 1:
            return recieved[0]
        else:
            return None

    def getParticipantByEmail(self, email):
        recieved = Participant.objects.filter(group_former=self,part_email=email)
        if len(recieved) > 1:
            raise ValueError('There are more than one '+email+' in '+str(self))
        if len(recieved) == 1:
            return recieved[0]
        else:
            return None
    
    def getRoster(self):
        recieved = Participant.objects.filter(group_former=self.pk)
        return recieved
    
    def getProjectList(self):
        recieved = Project.objects.filter(group_former=self.pk)
        return recieved

    def getAttributeList(self):
        recieved = Attribute.objects.filter(group_former=self.pk)
        return recieved
class Project(models.Model):
    group_former = models.ForeignKey(GroupFormer, on_delete = models.CASCADE)
    project_name = models.CharField(max_length=240, blank=False, null=False)
    project_description = models.TextField(blank=False, null=False)
    
    def __str__(self):
        return self.project_name + ' (' + str(self.group_former) + ')'
    
    def getParticipantChoice(self, participant):
        return participant.getProjectChoice(self)

class Attribute(models.Model):
    group_former = models.ForeignKey(GroupFormer, on_delete = models.CASCADE)
    attr_name = models.CharField(max_length=100)
    is_homogenous = models.BooleanField()
    is_continuous = models.BooleanField()
    
    def __str__(self):
        return self.attr_name + ' (' + str(self.group_former) + ')'
    
    def getParticipantChoice(self, participant):
        return participant.getAttributeChoice(self)

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
        return participantDesiredPartner(self,p)
    
    """
        Helper functions to get selections
    """
    def getDesiredPartnerList(self):
        recieved = self.desired_partner.filter(participant=self.pk)
        return recieved
    def getAttributeChoice(self, attribute):
        recieved = attribute_selection.objects.filter(participant=self,attribute=attribute)
        if len(recieved) > 1:
            raise TypeError(str(self)+" has more than one selection for "+str(attribute))
        if len(recieved) == 1:
            return recieved[0]
        else:
            return None
    
    def getProjectChoice(self, project):
        recieved = project_selection.objects.filter(participant=self,project=project)
        if len(recieved) > 1:
            raise TypeError(str(self)+" has more than one selection for "+str(project))
        if len(recieved) == 1:
            return recieved[0]
        else:
            return None

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
       WARNING: If a duplicate name or email is found, will silently not add, since atm no logging system exists!
    """
    ps = []
    for (name,email) in roster:
        try:
            ps = ps + [addParticipant(gf,name,email)]
        except ValueError:
            pass
            #Raise a warning to the proper channels
    return ps

""" 
    Each of the following takes the required attributes
    Of their associated model, and returns an instance of that model
    after adding it to the database
"""

def addGroupFormer(name,email,section):
    if getGroupFormer(name,section) != None:
        raise ValueError("GroupFormer with name "+name+" and section "+section+" already exists")
    p = GroupFormer.objects.create(prof_name=name,
                                   prof_email=email,
                                   class_section=section)
    return p

def addAttribute(gf, name, is_homogenous, is_continuous):
    if gf.getAttribute(name) != None:
        raise ValueError("Attribute "+name+" already exists in "+str(gf))
    p = Attribute.objects.create(group_former=gf,
                                 attr_name=name,
                                 is_homogenous=is_homogenous,
                                 is_continuous=is_continuous)
    return p

def addProject(gf, name, description):
    if gf.getProject(name):
        raise ValueError("Project "+name+" already exists in "+str(gf))
    p = Project.objects.create(group_former=gf,
                               project_name=name,
                               project_description=description)
    return p

def addParticipant(gf, name, email):
    if gf.getParticipantByName(name) != None or gf.getParticipantByEmail(email) != None:
        raise ValueError("Participant "+name+" or email "+email+" already exists in "+str(gf))
    p = Participant.objects.create(group_former=gf,
                                   part_name=name,
                                   part_email=email)
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
    if participant.getAttributeChoice(attribute) != None:
        raise ValueError(str(participant)+" has already selected a value for "+str(attribute))
    
    p = attribute_selection.objects.create(participant=participant,
                                           attribute=attribute,
                                           value=value)
    participant.attributes.add(attribute,through_defaults={'value':value})
    return p

def participantProjectChoice(participant,project,value):
    # Required that both participant and project be in the same GroupFormer
    if participant.group_former != project.group_former:
        raise ValueError(str(participant)+" and "+str(project)+" are not part of the same GroupFormer")
    if participant.getProjectChoice(project) != None:
        raise ValueError(str(participant)+" has already selected a value for "+str(project))
        
    p = project_selection.objects.create(participant=participant,
                                         project=project,
                                         value=value)
    participant.projects.add(project,through_defaults={'value':value})
    return p

"""
    Adds an instance of the desired partner relation
    :param wanter: the Participant who wishes to work with the wantee
    :param wantee: the Participant who is wished to be worked with
    :return: the list of desired partners of wanter
"""
def participantDesiredPartner(wanter,wantee):
    #Required that both participants are in the same GroupFormer
    if wanter.group_former != wantee.group_former:
        raise ValueError(str(wanter)+" and "+str(wantee)+" are not part of the same GroupFormer")
    
    wanter.desired_partner.add(wantee)
    
    return wanter.desired_partner

"""
    Allows for getting a GroupFormer from the instructor's name and the section
"""
def getGroupFormer(name, section):
    selection = GroupFormer.objects.filter(prof_name=name,class_section=section)
    if len(selection) > 1:
        raise ValueError("There are more than one GroupFormer under "+name+" called "+section)
    if len(selection) == 1:
        return selection[0]
    else:
        return None
