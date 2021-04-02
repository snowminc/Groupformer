from django.test import TestCase

from dbtools.models import *

# Create your tests here.

class DatabaseTests(TestCase):
    def test_setup(self):
        #Setup a basic structure
        g = GroupFormer.objects.create(prof_name="Test Prof",prof_email="test@uni.edu",class_section="DEPT101")
        g.save()
        Attribute.objects.create(group_former=g,attr_name="Attr Name 1",is_homogenous=False,is_continuous=True)
    
    def test_adding(self):
        #Add various additional entities and relationships
        pass
    
    def test_removing(self):
        #Remove different elements and test their outputs
        pass
    
    def test_cleanup(self):
        #Clear database by removing GroupFormers
        pass
