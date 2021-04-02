from django.test import TestCase

from dbtools.models import *

# Create your tests here.

class DatabaseTests(TestCase):
    def test_basic(self):
        #Setup a basic set of each
        print("Adding database elements manually (.objects.create() and .save())")
        gf = GroupFormer.objects.create(prof_name="Test Prof",prof_email="test@uni.edu",class_section="DEPT101")
        gf.save()
        attr = Attribute.objects.create(group_former=gf,attr_name="Attr Name 1",is_homogenous=False,is_continuous=True)
        attr.save()
        proj = Project.objects.create(group_former=gf,project_name="Project One",project_description="A description!")
        proj.save()
        part = Participant.objects.create(group_former=gf,part_name="Participant Name",part_email="joe@umbc.edu")
        part.save()
        
        print("Adding with helper functions")
        gf2 = addGroupFormer("Petra","pnadir@umbc.edu","Grass watching")
        
        
    
    def test_adding(self):
        #Add various additional entities and relationships
        pass
    
    def test_removing(self):
        #Remove different elements and test their outputs
        pass
    
    def test_cleanup(self):
        #Clear database by removing GroupFormers
        pass
