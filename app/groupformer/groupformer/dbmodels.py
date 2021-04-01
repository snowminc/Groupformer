# Based on Kristian's branch we appear to be working towards having
# different apps for setup and response screens, so this is generalized

# Use the following to import this file
# from groupformer import dbmodels

from django.db import models

#Entities

class GroupFormer(models.Model):
    prof_name = models.CharField(max_length=200)
    prof_email = models.CharField(max_length=200)
    class_section = models.CharField(max_length=100)
    
    def __str__(self):
        return class_section + ' ' + prof_name 

class Project(models.Model):
    # Required to test relation involving it
    # To be replaced by Sarah's
    gf = models.ForeignKey(GroupFormer, on_delete = models.CASCADE)
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000)

class Attribute(models.Model):
    gf = models.ForeignKey(GroupFormer, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    is_homogenous = models.BooleanField()
    is_continuous = models.BooleanField()
    
    def __str__(self):
        return name
    

class Participant(models.Model):
    gf = models.ForeignKey(GroupFormer, on_delete = models.CASCADE)
    part_email = models.CharField(max_length=200)
    part_name = models.CharField(max_length=200)
    
    def __str__(self):
        return name

# Relationships

class attribute_selection(models.Model):
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete = models.CASCADE)
    value = models.IntegerField()

class project_selection(models.Model):
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    value = models.FloatField()

class desired_partner(models.Model):
    wisher = models.ForeignKey(Participant, on_delete = models.CASCADE)
    wishee = models.ForeignKey(Participant, on_delete = models.CASCADE)

