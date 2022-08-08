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

import DB_manage

current_dir = os.getcwd()

database_name = "database_IBM.txt"
logfile_name = "logfile_IBM.txt"
tmpfile_name = "tmp.txt"
prog_files = [database_name,tmpfile_name,logfile_name,]

# initialise object dictionary ????
object_dict = {}
# this will re-initialise every time the program is run
# could use pickle module to re-import objects when file opens to repopulate a dict as a solution to this

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
    DB_manage.updateLog(obj_name,DB_manage.getTime(),DB_manage.getDate(),"add")
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
                DB_manage.updateLog(obj_name,DB_manage.getTime(),DB_manage.getDate(),"delete")
     
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


#files_found = DB_manage.findBackUps(current_dir)
#corrupt_status = DB_manage.checkBackUps(files_found)
#DB_manage.initDatabase(corrupt_status)
#initDatabase(corrupt_status)
#initDatabase(recovered)
# example functions - all will report to log
#LEMON = addObject("LEMON","round yellow citrus friut")
#PEAR = addObject("PEAR","strange squishy friut")
#deleteObject("PEAR")