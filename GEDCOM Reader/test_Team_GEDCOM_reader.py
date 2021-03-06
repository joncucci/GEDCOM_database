import unittest
from Team_GEDCOM_reader import *

class TestGEDCOMReader(unittest.TestCase):

    #Checking marriage befpre death
    def test_marr_before_div(self):
        self.assertTrue(families[0].divorced == "2003-02-18", msg="Error1")
        self.assertTrue(families[1].divorced == "INVALID DATE", msg="Error2")
        self.assertTrue(families[2].divorced == "NA", msg="Error3")
        self.assertTrue(families[3].divorced == "NA", msg="Error4")
        self.assertTrue(families[4].divorced == "2010-04-13", msg="Error5")

    #Checking marriage before death date
    def test_marr_before_deat(self):
        self.assertTrue(families[0].married == "1992-03-22", msg="Error1")
        self.assertTrue(families[1].married == "INVALID DATE", msg="Error2")
        self.assertTrue(families[2].married == "1969-02-2", msg="Error3")
        self.assertTrue(families[3].married == "INVALID MARRIAGE AGE", msg="Error4")
        self.assertTrue(families[4].married == "1994-04-13", msg="Error5")

    #Checking Individuals existence
    def test_individual(self):
        self.assertIsNotNone(individuals[-1], msg=None)

    #Seeing if Birth Date Exists
    def test_birtCheck(self):
        self.assertTrue(birt_check, msg=None)

    #Seeing if Birth Date fills to date time correctly
    def test_birtDate(self):
        self.assertIsNotNone(birt_obj, msg=None)

    #Seeing if Death Date Exists
    def test_deatCheck(self):
        self.assertTrue(deat_check, msg=None)

    #Seeing if Death Date fills to date time correctly
    def test_deatDate(self):
        self.assertIsNotNone(deat_obj, msg=None)
        
    # Checks to see if individual ID matches the GEDCOM file
    def individual_ID(self):
        self.assertEqual(individuals[0].ID, "I1")

    # Checks to see if fam ID matches GEDCOM file, as well as the husband and wife IDs and Names.
    def family_ID(self):
        self.assertEqual(families[0].ID, "F1")
        self.assertEqual(families[0].husband_id, "I1")
        self.assertEqual(families[0].wife_id, "I2")

    # Testing to see if Children match to the correct family
    def family_children(self):
        self.assertEqual(families[1].ID, "F2")
        self.assertEqual(families[1].children, ["I1", "I5"])

    # Testing to ensure Unique Individual IDs
    def unique_individual_IDs(self):
        unique_IDs = []
        for num in range(len(individuals)):
            unique_IDs.append(individuals[num].ID)
        for ID in range(len(unique_IDs)):
            self.assertEqual(unique_IDs.count(unique_IDs[ID]), 1)

    # Testing to ensure Unique Family IDs
    def unique_family_IDs(self):
        unique_Fam_IDs = []
        for num in range(len(families)):
            unique_Fam_IDs.append(families[num].ID)
        for ID in range(len(unique_Fam_IDs)):
            self.assertEqual(unique_Fam_IDs.count(unique_Fam_IDs[ID]), 1)

        
if __name__ == '__main__':
    unittest.main()                        
