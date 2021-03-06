'''
@Author: Jonathan Cucci, Joe Letizia, Markell Torres, Erik Buczek
SSW555 Proj-2
GEDCOM Reader
'''
from Person import *
from Family import *
import os.path
from os import path
from datetime import *
import datetime
import sqlite3
from functions import *
today = str(datetime.date.today())
today = str(datetime.date.today())

# Opens GEDCOM file as fam variable
with open('Letizia_GEDTEST.ged.txt') as fam:
    text = fam.readlines()
    # Tags broken down into indexes that correspond with their acceptable level number
    tags = [["INDI", "FAM", "HEAD", "TRLR", "NOTE"],["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"],["DATE"]]
    months = {
        'JAN' : "01",
        'FEB' : "02",
        'MAR' : "03",
        'APR' : "04",
        'MAY' : "05",
        'JUN' : "06",
        'JUL' : "07",
        'AUG' : "08",
        'SEP' : "09",
        'OCT' : "10",
        'NOV' : "11",
        'DEC' : "12"}
    individuals = []
    families = []
    line_point = 0

    # Goes through each line of the GEDCOM file
    for line in text:
        newLine = line.split()
        if ("INDI" in newLine):
            # pointer += 1
            individuals.append(Person())
            individuals[-1].ID = newLine[1][1:-1]
        elif("NAME" in newLine):
            individuals[-1].name = newLine[-2] + " " + newLine[-1][1:-1]
        elif("SEX" in newLine):
            individuals[-1].gender = newLine[-1]
        elif("BIRT" in newLine):
            next_line = line_point + 1
            next_line = text[next_line].split()
            birt_date = next_line[-1] + "-" + months[next_line[-2]] + "-" + next_line[-3]
            try:
                if(birt_date > today):
                    individuals[-1].birthday = "INVALID DATE"
                else:
                    individuals[-1].birthday = birt_date
            except KeyError:
                individuals[-1].birthday = next_line[-1]

            #US02/US03: Birth before Marriage/Death
            birt_check = False
            try:
                birt_obj = datetime.datetime.strptime(individuals[-1].birthday, '%Y-%m-%d')
                birt_check = True
            except:
                pass

        elif("DEAT" in newLine):
            individuals[-1].alive = False
            next_line = line_point + 1
            next_line = text[next_line].split()
            deat_date = next_line[-1] + "-" + months[next_line[-2]] + "-" + next_line[-3]
            if("DATE" not in next_line):
                individuals[-1].death = "Not Found"
            else:
                try:
                    if(deat_date > today):
                        individuals[-1].death = "INVALID DATE"
                    else:
                        individuals[-1].death = deat_date
                except KeyError:
                    individuals[-1].death = next_line[-1]

            #US03: Birth before Death
            deat_check = False
            try:
                deat_obj = datetime.datetime.strptime(individuals[-1].death, '%Y-%m-%d')
                deat_check = True
            except:
                pass

            if (birt_check == True and deat_check == True and birt_obj.date() < deat_obj.date()):
                pass
            else:
                individuals[-1].death = "INVALID DATE"
                print("Individual ID: "+individuals[-1].ID+" | INVALID INDIVIDUAL: death before birth")

        elif("FAM" in newLine):
            families.append(Family())
            families[-1].ID = newLine[1][1:-1]

        elif("HUSB" in newLine):
            next_line = text[line_point+1].split()
            families[-1].husband_id = newLine[-1][1:-1]
            families[-1].wife_id = next_line[-1][1:-1]
            for person in individuals:
                if person.ID == families[-1].husband_id:
                    families[-1].husband_name = person.name
                    #US21: Correct gender for role
                    if(person.gender == "F"):
                        person.gender = "INVALID GENDER"
                    person.spouse.append(families[-1].wife_id)

        elif("WIFE" in newLine):
            prev_line = text[line_point-1].split()
            families[-1].wife_id = newLine[-1][1:-1]
            families[-1].husband_id = prev_line[-1][1:-1]
            for person in individuals:
                if person.ID == families[-1].wife_id:
                    families[-1].wife_name = person.name
                    #US21: Correct gender for role
                    if(person.gender == "M"):
                        person.gender = "INVALID GENDER"
                    person.spouse.append(families[-1].husband_id)

        elif("CHIL" in newLine):
            families[-1].children.append(newLine[-1][1:-1])
            for person in individuals:
                if person.ID == families[-1].husband_id:
                    person.child.append(newLine[-1][1:-1])
                if person.ID == families[-1].wife_id:
                    person.child.append(newLine[-1][1:-1])

        elif("DIV" in newLine):
            if "DATE" in text[line_point+1].split():
                next_line = text[line_point+1].split()
                marr_date = text[line_point-1].split()
                div_date = next_line[-1] + "-" + months[next_line[-2]] + "-" + next_line[-3]

                for person in individuals:
                    if person.ID == families[-1].husband_id:
                        temp_husband_death = person.death
                    if person.ID == families[-1].wife_id:
                        temp_wife_death = person.death
                try:
                    if(div_date > today):
                        families[-1].divorced = "INVALID DATE"
                    elif(div_date > temp_wife_death or div_date > temp_husband_death):
                        families[-1].divorced = "INVALID DATE"

                    #US04: Marriage before divorce
                    elif(next_line[-3:] == marr_date[-3:] or next_line[-1] > marr_date[-1] or (next_line[-1] == marr_date[-1] and months[next_line[-2]] > months[marr_date[-2]]) or (months[next_line[-2]] == months[marr_date[-2]] and next_line[-3] > marr_date[-3])):
                        families[-1].divorced = next_line[-1] + "-" + months[next_line[-2]] + "-" + next_line[-3]
                    else:
                        families[-1].divorced = "INVALID DATE"
                except KeyError:
                    families[-1].divorced = next_line[-1]
            else:
                families[-1].divorced = "Date not found"

        elif("MARR" in newLine):
            if "DATE" in text[line_point+1].split():
                next_line = text[line_point+1].split()
                marr_date_string = next_line[-1] + "-" + months[next_line[-2]] + "-" + next_line[-3]
                marr_date_array = [next_line[-3], months[next_line[-2]], next_line[-1]]

                for person in individuals:
                    if person.ID == families[-1].husband_id:
                        temp_husband_birth = person.birthday
                        temp_husband_birth_date = datetime.datetime.strptime(person.birthday, '%Y-%m-%d')
                        marriage_date = datetime.datetime.strptime(marr_date_string, '%Y-%m-%d')
                        husband_age = marriage_date.year - temp_husband_birth_date.year - ((marriage_date.month, marriage_date.day) < (temp_husband_birth_date.month, temp_husband_birth_date.day))

                    if person.ID == families[-1].wife_id:
                        temp_wife_birth = person.birthday
                        temp_wife_birth_date = datetime.datetime.strptime(person.birthday, '%Y-%m-%d')
                        marriage_date = datetime.datetime.strptime(marr_date_string, '%Y-%m-%d')
                        wife_age = marriage_date.year - temp_wife_birth_date.year - ((marriage_date.month, marriage_date.day) < (temp_wife_birth_date.month, temp_wife_birth_date.day))
                try:
                    if(marr_date_string > today):
                        families[-1].married = "INVALID DATE"
                    elif(husband_age < 14 or wife_age < 14):
                        families[-1].married = "INVALID MARRIAGE AGE"
                    elif(temp_husband_birth > marr_date_string or temp_wife_birth > marr_date_string):
                        families[-1].married = "INVALID DATE"
                        print("Family ID: "+families[-1].ID+" | INVALID INDIVIDUAL: marriage before birth")
                    else:
                        families[-1].married = marr_date_string
                except KeyError:
                    families[-1].married = next_line[-1]

            #US05: Marriage before death
                if(individuals[-1].alive == False):
                    deat_date = individuals[-1].death.split("-")
                elif(individuals[-2].alive == False):
                    deat_date = individuals[-2].death.split("-")
                try:
                    if(individuals[-1].alive == False or individuals[-2].alive == False):
                        if(families[-1].married == "INVALID DATE"):
                            pass
                        elif(families[-1].married == "INVALID MARRIAGE AGE"):
                            pass
                        elif(marr_date_array[2] > deat_date[0] or (marr_date[2] == deat_date[0] and marr_date[1] > deat_date[1]) or (marr_date[1] == deat_date[1] and marr_date[0] > deat_date[2])):
                            families[-1].married = "INVALID DATE"
                            families[-1].divorced = "INVALID DATE"
                        else:
                            families[-1].married = marr_date_array[2] + "-" + marr_date_array[1] + "-" + marr_date_array[0]
                    elif(families[-1].married == "INVALID DATE"):
                        pass
                    elif(families[-1].married == "INVALID MARRIAGE AGE"):
                        pass
                    else:
                        families[-1].married = next_line[-1] + "-" + months[next_line[-2]] + "-" + next_line[-3]
                except KeyError:
                    families[-1].married = next_line[-1]


        line_point += 1


    # Updates everyones age
    for individual in individuals:

        today = date.today()
        if (individual.birthday != "INVALID DATE"):
            birth = individual.birthday.split('-')
            birth = date(int(birth[0]), int(birth[1]), int(birth[2]))

        if individual.birthday == "NA":
            individual.age = 0

        elif individual.death == "NA":
            individual.age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

        elif (individual.death != "NA" and individual.death != "INVALID DATE"):
            death = individual.death.split('-')
            death = date(int(death[0]), int(death[1]), int(death[2]))
            individual.age = death.year - birth.year - ((death.month, death.day) < (birth.month, birth.day))

        else:
            individual.age = 0

        if (individual.age >= 150):
            individual.age = "INVALID AGE"

    #Formatting between Validity Checks and Individual/Family List
    print()
    print("----------------------------------------------------------------------------------------------------------------------------")
    print()
    
    #US40: Include input line numbers
    line_count = 0
    
    for person in individuals:
        info = vars(person)
        print(line_count,', '.join("%s: %s" % value for value in info.items()))
        line_count += 1

    for family in families:
        info_f = vars(family)
        print(line_count,', '.join("%s: %s" % value for value in info_f.items()))
        line_count += 1

    conn = sqlite3.connect('GEDCOM.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS INDIVIDUALS")
    c.execute("DROP TABLE IF EXISTS FAMILIES")

    c.execute(''' CREATE TABLE INDIVIDUALS (
                    [ID] TEXT PRIMARY KEY, 
                    [name] TEXT, 
                    [gender] TEXT,
                    [birthday] TEXT, 
                    [age] INTEGER, 
                    [alive] BOOLEAN, 
                    [death] TEXT, 
                    [children] TEXT,
                    [spouse] TEXT
            )''')
        
    c.execute(''' CREATE TABLE FAMILIES (
                    [ID] TEXT PRIMARY KEY, 
                    [married] TEXT, 
                    [divorced] TEXT,
                    [husband_id] TEXT, 
                    [husband_name] TEXT, 
                    [wife_id] TEXT, 
                    [wife_name] TEXT,
                    [children] TEXT
            )''')

    for person in individuals:

        info = list(vars(person).values())
        #print(info)
        for index in range(len(info)):
            if type(info[index]) is list:
                info[index] = ", ".join(ids_to_names(info[index], individuals))
        #print(info)

        
        sql = '''INSERT INTO INDIVIDUALS (ID, name, gender, birthday, age, alive, death, children, spouse)
                 VALUES(?,?,?,?,?,?,?,?,?)'''
        c.execute(sql, info)


    for family in families:

        info = list(vars(family).values())
        #print(info)
        for index in range(len(info)):
            if type(info[index]) is list:
                info[index] = ", ".join(ids_to_names(info[index], individuals))
        #print(info)
        sql = '''INSERT INTO FAMILIES (ID, married, divorced, husband_id, husband_name, wife_id, wife_name, children)
                 VALUES(?,?,?,?,?,?,?,?)'''

        c.execute(sql, info)

    conn.commit()
    print("successful")

'''
        # if there is a tag in the first index value that can be found
        # in the TAG list corresponding its level val and manipulate
        #  the string to add Y
        if(newLine[1] in tags[int(newLine[0])]):
            newLine[1] = "|" + newLine[1] + "|" + "Y|"
        # Else if the list after slicing is larger than 2 pieces, and the
        # index 2 element is in the TAGS list with a corresponding level value,
        # change the 1st index to the tag and put the id after
        elif(len(newLine) > 2 and newLine[2] in tags[int(newLine[0])]):
            temp = newLine[2]
            newLine[2] = newLine[1]
            newLine[1] = "|" + temp + "|" + "Y|"
        # Else, manipulate index 1 to add N. It is not a compatable TAG.
        else:
             newLine[1] = "|" + newLine[1] + "|" + "N|"
        # Input / Output formatting
        line = "--> " + line
        printLine = "<--"
        # Concatenation
        for bit in newLine:
            printLine = printLine + " " + bit
        # Annnnnnnnd Print
        print(line[:-1])
        print(printLine + "\n")
'''
