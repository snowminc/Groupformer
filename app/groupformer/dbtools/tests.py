from django.test import TestCase

from dbtools.models import *

class DatabaseTests(TestCase):
    def test_basic(self):
        #Setup a basic set of each
        
        # Manual addition
        print("Adding database elements manually (.objects.create() and .save())")
        gf = GroupFormer.objects.create(prof_name="Test Prof",prof_email="test@uni.edu",class_section="DEPT101")
        gf.save()
        attr = Attribute.objects.create(group_former=gf,attr_name="Attr Name 1",is_homogenous=False,is_continuous=True)
        attr.save()
        proj = Project.objects.create(group_former=gf,project_name="Project One",project_description="A description!")
        proj.save()
        part = Participant.objects.create(group_former=gf,part_name="Participant One",part_email="joe@umbc.edu")
        part.save()
        
        # Standalone Helper function addition
        print("Adding with helper functions (add...(gf,))")
        gf2 = addGroupFormer("Petra","pnadir@umbc.edu","Grass watching")
        attr2 = addAttribute(gf2,"An Attribute",False,False)
        proj2 = addProject(gf2,"On top of the hill","This grass needs to be watched")
        part2 = addParticipant(gf2,"In dividual","one@unl.edu")
        part22= addParticipant(gf2,"Alicia V","avan@umbc.edu")
        participantAttributeChoice(part2,attr2,5)
        with self.assertRaises(ValueError) as cm:
            participantProjectChoice(part,proj2,2)
        print(cm.exception)
        print("Exception succeeded")
        participantDesiredPartner(part2,part22)
        participantProjectChoice(part2,proj2,3)
        
        addRoster(gf2,[["Alfred Person","e@mail.com"],["Ta Person","two@names.info"]])
        
        # Class Helper function addition
        print("Adding with class helper functions (gf.add...())")
        gf.addProject("Project 2","A description!")
        attr12=gf.addAttribute("Amount of cheese",True,False)
        part12=gf.addParticipant("Morgan","mv@george.biz")
        part12.attributeChoice(attr12,5)
        part12.projectChoice(proj,1)
        part12.desires(part)
        
        gf2.addRoster([["Morrison Person","np@person.com"],["Eve Person","jp@upl.edu"]])
        gf.addParticipant("Alicia V","avan@umbc.edu")
        Participant.objects.filter(part_name="Eve Person")[0].desires(part22)
        Participant.objects.filter(part_name="Eve Person")[0].desires(part2)
        Participant.objects.filter(part_name="Eve Person")[0].desires(
            Participant.objects.filter(part_name="Morrison Person")[0])
        with self.assertRaises(ValueError):
            #Incorrect GroupFormer
            Participant.objects.filter(part_name="Eve Person")[0].desires(
                Participant.objects.filter(part_name="Alicia V",group_former=gf)[0])
        
        # Database printing
        print("Printing database\n-----------------")
        gfset = GroupFormer.objects.all()
        for gfi in gfset:
            print(gfi)
            for proji in Project.objects.filter(group_former=gfi):
                print(proji)
            print()
            for attri in Attribute.objects.filter(group_former=gfi):
                print(attri)
            print()
            for parti in Participant.objects.filter(group_former=gfi):
                print(parti)
            print('--------')
        
        # Database Checking
        print("Check correctness")
        gfs = gfset.filter(prof_name="Petra")
        self.assertEqual(len(gfs),1)
        #GroupFormer Getter checks
        self.assertEqual(gf2.getProject("On top of the hill"),proj2)
        self.assertEqual(gf2.getProject("This doesn't exist!"),None)
        self.assertEqual(gf.getAttribute("Attr Name 1"), attr)
        self.assertEqual(gf2.getParticipant("Alicia V"),part22)
        self.assertNotEqual(gf.getParticipant("Alicia V"),None)
        self.assertNotEqual(gf.getParticipant("Alicia V"),part22)
        #Desired Partner
        self.assertIn(part,part12.desired_partner.all())
        part23 = Participant.objects.filter(part_name="Eve Person")[0]
        self.assertIn(part22,part23.desired_partner.all())
        print(part23.desired_partner.all())
        #Project Selection
        self.assertEqual(len(project_selection.objects.filter(participant=part2)),1)
        self.assertEqual(project_selection.objects.filter(participant=part2)[0].value,3)
        self.assertEqual(part2.getProjectChoice(proj2).value,3)
        self.assertEqual(proj2.getParticipantChoice(part2).value,3)
        #Attribute Selection
        self.assertEqual(attribute_selection.objects.filter(participant=part2,attribute=attr2)[0].value,5)
        self.assertEqual(part2.getAttributeChoice(attr2).value,5)
        self.assertEqual(attr2.getParticipantChoice(part2).value,5)
