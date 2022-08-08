# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 14:49:28 2022

@author: ellie
"""

import shutil
import os
import datetime as dt
import sys

from datetime import date
from os.path import exists

current_dir   = os.getcwd()
database_name = "database_IBM.txt"
logfile_name  = "logfile_IBM.txt"
tempfile_name = "temp_file.txt"

# initialise object dictionary ????
object_dict = {}
# this will re-initialise every time the program is run
# could use pickle module to re-import objects when file opens to repopulate a dict as a solution to this

def getDate():
    date_now = dt.datetime.today().strftime('%d-%m-%Y')
    return date_now

def getTime():       
    time_now = dt.datetime.today().strftime('%H:%M:%S')
    return time_now

def findBackUps(current_dir):
    # find current directory and form tmp file path
    recovered_file = current_dir + "/tmp.txt"
    # find if it exists
    if exists(recovered_file):
    # if exists, check for non-ASCII characters (corruption)
        with open(recovered_file,'rb') as check_file:
            # while there are chars to read
            while True:
                for line in check_file:
                    try:
                        line.decode("ascii")
                    except UnicodeDecodeError:
                        print("BAD LINE: " + str(line))
                        break
                    except:
                         print("UNKNOWN: " + str(line))
                         break
                    else:
                        # no non-ascii chars found - continue reading
                        pass
        return recovered_file
    # Base case - if no file to recover OR failed recovery, just return false
    return

def yesOrNoInput(stringRequest):
    while True:
        response = input(stringRequest).lower()
        if 'y' in response:
            return True
        elif 'n' in response:
            return False


def initDatabase(recovered):
    # if `recovered` exists, database was recovered
    if recovered:
        if yesOrNoInput("Proceed with recovered database? (Y/N)\n"):
            # continue appending database and logfile
            print("Proceeding with recovered database") # what if no log file found?
            # add message to logfile saying when file was recovered
            updateLog(None,getTime(),getDate(),"recover")
        else:
            # delete old database and logfile - stop hard coding these names and make them variables
            os.remove(current_dir + "/" + str(database_name))
            os.remove(current_dir + "/" + str(logfile_name))
            os.remove(current_dir + "/tmp.txt")
    # if no back-ups found start from scratch      
    else:
        # create empty text file using with open
        try:
            open(database_name, 'w')
            open(logfile_name, 'a+')
            updateLog("DATABASE", getTime(), getDate(), "create")
        except:
            print("ERROR CREATING DATABASE")
            sys.exit(1)

            
def updateLog(obj_name,log_time,log_date,action):
    # append latest action to logfile
    if action == "add" or "delete":
        with open(logfile_name, 'a') as l:
            # form and join log string
            log_string = ["--- Operation %s"%(action) + " %s"%(obj_name) + " applied to database at %s" %(log_time) + " on %s ---" %(log_date)]
            l.write("".join(log_string))
            l.write("\n")

    elif action == "recover":
        print("Adding recovered status to logfile")
        log_string = ["--- Database recovered from previous session at %s" %(log_time) + " on %s ---" %(log_date)]
        l.write("".join(log_string))
        l.write("\n")
    
    elif action == "create":
        print("Creating new logfile")
        log_string = ["--- New logfile created at %s" %(log_time) + " on %s ---" %(log_date)]
        l.write("".join(log_string))
        l.write("\n")
        
    else:
        print("INVALID DATABASE OPERATION")
        sys.exit(1)
    
    print("Reported change to logfile")


class Fruit:
    def __new__(cls, name):
        print(f"Creating a new {cls.__name__} object")
        obj = object.__new__(cls)
        return obj
    
    # constructor
    def __init__(self, atr):
        # initialise string property
        self.atr = atr
        print("Initialising new object with string attribute:\n" + str(self.atr))
        
    
def addObject(obj_name,atr):
    # first need to create a temp file to avoid data loss
    try:
        temp_file = shutil.copy(database_name,tempfile_name)
    except:
        print("FAILED TO COPY DATABASE FILE - do you have permission?")
        sys.exit(1)

    # need to check if a string - or make it one!
    obj = Fruit(atr)
    # add object to dict
    object_dict[obj_name] = obj.__dict__
    # add object representation to txt file
    with open(database_name, 'a') as f:
        data_string = ["%s" %(obj_name) + " with tag %s" %(obj) + " colour.%s = %s" % (atr) for atr in obj.__dict__.items()]
        f.write("".join(data_string))
        f.write("\n")
    print("Added " + obj_name + " object to database.")
    
    # update log
    updateLog(obj_name,getTime(),getDate(),"add")
    # now addition has been successfully performed - delete tmp_file
    os.remove(temp_file)
    print("Database safely updated")
    
    return obj
        
        
def deleteObject(obj_to_delete):
    # first need to create a temp file to avoid data loss
    try:
        temp_file = shutil.copy(database_name,tempfile_name)
    except:
        print("FAILED TO COPY DATABASE FILE - do you have permission?")
        sys.exit(1)
    # need to delete this object from RAM in here and the current file. 
    #del object_dict[obj_to_delete]
    # need to find and delete object in file first
    with open(database_name, 'r') as oldfile, open('new_database_IBM.txt', 'w') as newfile:
        for line in oldfile.readlines():
            if str(obj_to_delete) != line.split(maxsplit=1)[0]:
                newfile.write(line)
            # update log file
            else:
                obj_name = obj_to_delete
                # update log
                updateLog(obj_name,getTime(),getDate(),"delete")
     
    # action performed successfully - now delete old database 
    os.remove(database_name)
    # and rename new database
    os.rename("new_database_IBM.txt",database_name)
    # now deletion has been successfully performed - delete tmp_file
    os.remove(temp_file)
    print("Database safely updated")
    
    
# quick function to test my test_file
def add(a,b):
    return a+b


if exists(database_name):
    if yesOrNoInput("Database discovered, would you like to overwrite it? (Y/N)\n"):
        if yesOrNoInput("Are you sure? Database will be overwritten (Y/N)\n"):
            print("Database overwritten")
            initDatabase(findBackUps(current_dir))
else:
    initDatabase(findBackUps(current_dir))


# example functions - all will report to log
LEMON = addObject("LEMON","round yellow citrus fruit")
PEAR = addObject("PEAR","strange squishy fruit")
deleteObject("PEAR")