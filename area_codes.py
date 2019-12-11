import time
from acctmis import *


CODES = {}
AREACODE = "https://www.bennetyee.org/ucsd-pages/area.html"

#Reads the website with areacodes and gets the table on the website and stores table into magic dictionary CODES. 
def get_area_codes():
    soup = get_web_page(AREACODE)
    table_list = get_table(soup)
    for i, row in enumerate(table_list[1]):
        CODES[table_list[i][0]] = [table_list[i][1],table_list[i][2],table_list[i][3]] #there is an error here, I need it to pull the entire table, not just the first three values
    if True:
        return "True"
    else:
        print("Error. Verify code.")
        return "False"

#Verifies whether get_area_codes has been run and verifies whether the input is valid
#Looking for: string with a length of 3, whether the value is in the global dictonary
#The code below returns the state code as string
def get_state_for_code(n):
    if CODES == {}:
        print("Error. Please run get_area_codes function first")
    else:
        if type(n) == str:
            if len(n) == 3:
                if n in CODES.keys():
                    return str(CODES[n][0])
                else:
                    print("Error. Not found in dictionary")
                    return "None"
            else:
                print("Error. Length of string must be three")
                return "None"
        else:
            print("Error. Input is not a string")
            return "None"

#Verifies whether get_area_codes has been run and verifies whether the input is valid
#Verifies whether string or integer, and prints error if otherwise
#Takes Integer, checks for a length of 10, checks if the first 3 digits is a key in the dictionary CODES, and returns all data about the area code
#Take string, check for length of 10,12,14, check for 10 digits in the string, checks for valid formatting, and checks if first 3 digits is a key in the CODES dictionary, returns data about area code.
#Prints errors and reason for error, and return none.
def get_data_for_number(n):
    if CODES == {}:
        print("Error, Please run get_area_codes function first")
    else:
        if type(n) == int:
            if len(str(n)) == 10:
                if str(n)[0:3] in CODES.keys():
                    return CODES[str(n)[0:3]]
                else:
                    print("Error. Not found in dictionary")
                    return "None"
            else:
                print("Error. Number must be 10 digits, example XXXXXXXXXX")
                return "None"
        elif type(n) == str:    
            if len(n) == 14:
                if sum(x.isdigit() for x in n) == 10:
                    if n[0] == "(" and n[1:4].isdigit() and n[4] == ")" and n[5] == " " and n[6:9].isdigit() and n[9] == " " and n[10:14].isdigit():
                        if n[1:4] in CODES.keys():
                            return CODES[n[1:4]]
                        else:
                            print("Error, not found in dictionary")
                            return "None"
                    else:
                        print("Error. Not valid format. Try string in format '(XXX) XXX XXXX'")
                        return "None"
                else:
                    print("Error. String must be exactly 10 digits ")
                    return "None"
            elif len(n) == 10:
                    if n[0:10].isdigit():
                        if n[0:3] in CODES.keys():
                            return CODES[n[0:3]]
                        else:
                            print("Error. Not found in dictionary")
                            return "None"
                    else:
                        print("Error. String must be exactly 10 digits. Try 'XXXXXXXXXX'")
                        return "None"
            elif len(n) == 12:
                if sum(x.isdigit() for x in n) == 10:
                    if n[0:3].isdigit() and n[3] == "-" and n[4:7].isdigit() and n[7] == "-" and n[8:12].isdigit():
                        if n[0:3] in CODES.keys():
                            return CODES[n[0:3]]
                        else:
                            print("Error. Not found in dictionary")
                            return "None"
                    else:
                        print("Error. Not valid format. Try string in this format 'XXX-XXX-XXXX'")
                        return "None"
                else:
                    print("Error. String must be exactly 10 digits.")
                    return "None"
            else:
                print("Error. String not appropriate length, example is 10, 12, or 14")
                return "None"
        else:
            print("Error. Input is not a string or integer")
            return "None"
        
    
