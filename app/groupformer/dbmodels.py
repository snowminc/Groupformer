# Based on Kristian's branch we appear to be working towards having
# different apps for setup and response screens, so this is generalized

# Use the following to import this file
# from .. import dbmodels

from django.db import Model

#Entities

class GroupFormer(models.Model):
    prof_name = models.CharField(max_length=100)
    prof_email = models.CharField(max_length=100)
    class_section = models.CharField(max_length=100)
    
    def __str__(self):
        return class_section + ' ' + prof_name 

class Attribute(models.Model):

class Participant(models.Model):

# Relationships

class attribute_selection(models.Model):

class project_selection(models.Model):

class desired_partner(models.Model):