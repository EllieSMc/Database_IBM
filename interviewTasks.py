# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 14:49:28 2022

@author: ellie
"""

import shutil
import datetime as dt
from datetime import date
import os
from os.path import exists

current_dir = os.getcwd()

database_name = "database_IBM.txt"
logfile_name = "logfile_IBM.txt"

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
    
# WRITE TESTS FOR THIS FUNCTION WITH DIFFERENT INITIAL FOLDERS # 
def findBackUps(current_dir):
    # find current directory and form tmp file path
    tmp_path = current_dir + "\\" + "tmp.txt"
    # find if it exists
    if exists(tmp_path) == True:
    # if exists, check for non-ASCII characters (corruption)
        recovered = tmp_path
        with open(tmp_path,'rb') as check_file:
            # while there are chars to read
            while True:
               for line in check_file:
                   try:
                       line.decode("ascii")
                   except UnicodeDecodeError:
                       print("BAD LINE: " + str(line))
                       recovered = False
                   else:
                       # no non-ascii chars found - continue reading
                       pass
    return recovered
 

def initDatabase(recovered):
    # if no back-ups found start from scratch
    if recovered == False:
        print("No file recovered - generating new storage file and log file")
        # create empty text file using with open
        with open(database_name, 'w') as my_new_text_file:
            pass
        with open(logfile_name, 'w') as my_new_logfile:
            pass
        updateLog("DATABASE", getTime(), getDate(), "create")
            
    else:
        print("Proceed with recovered database? (Y/N)")
        response = input()
        # act on response
        if response == "Y":
            # continue appending database and logfile
            print("Proceeding with recovered database") # what if no log file found?
            # add message to logfile saying when file was recovered
            updateLog(None,getTime(),getDate(),"recover")
        elif response == "N":
            # delete old database amd logfile - stop hard coding these names and make them variables
            os.remove(current_dir+"\\\\"+str(database_name))
            os.remove(current_dir+"\\\\"+str(logfile_name))
            os.remove(current_dir+"\\\\tmp.txt")
            
        else:
            print("Please enter a valid Y/N response")
            
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
        print("Invalid action")
    
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
    temp_file = shutil.copy("database_IBM.txt",current_dir+"\\\\temp_file.txt")
    # need to check if a string - or make it one!
    obj = Fruit(atr)
    # add object to dict
    object_dict[obj_name] = obj.__dict__
    # add object representation to txt file
    with open(database_name, 'a') as f:
        data_string = ["%s" %(obj_name) + " with tag %s" %(obj) + " colour.%s = %s" % (atr) for atr in obj.__dict__.items()]
        f.write("".join(data_string))
        f.write("\n")
    print("Added " + str(obj) + " object to .txt file.")
    
    # update log
    updateLog(obj_name,getTime(),getDate(),"add")
    # now addition has been successfully performed - delete tmp_file
    os.remove(temp_file)
    print("Database safely updated")
    
    return obj
        
        
def deleteObject(obj_to_delete):
    # first need to create a temp file to avoid data loss
    temp_file = shutil.copy(database_name,current_dir+"\\\\temp_file.txt")
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
    os.remove(current_dir+"\\\\"+str(database_name))
    # and rename new database
    os.rename("new_database_IBM.txt",str(database_name))
    # now deletion has been successfully performed - delete tmp_file
    os.remove(temp_file)
    print("Database safely updated")
    
    
# quick function to test my test_file
def add(a,b):
    return a+b





recovered = findBackUps(current_dir)
initDatabase(recovered)