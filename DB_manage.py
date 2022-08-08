# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 13:22:09 2022

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
tmpfile_name = "tmp.txt"
prog_files = [database_name,tmpfile_name,logfile_name]

# # # # SUPPORTING FUNCTIONS # # # #

def getDate():
    date_now = dt.datetime.today().strftime('%d-%m-%Y')
    return date_now

def getTime():       
    time_now = dt.datetime.today().strftime('%H:%M:%S')
    return time_now

def deleteOld():
    print("Deleting any leftover corrupted files")
    for i in range(0,len(prog_files)):
        try:
            os.remove(prog_files[i])
            # check this works without needing full path
        except:
            print("%s doesn't exist to delete - skip" %(prog_files[i]))
    print("Old files deleted") 
    
def createNew():
    print("Generating new storage file and log file")
    # create empty text file using with open
    with open(database_name, 'w') as my_new_text_file:
        pass
    with open(logfile_name, 'w') as my_new_logfile:
        pass
    updateLog("DATABASE", getTime(), getDate(), "create")
    
    
    
# # # # MAIN DATABASE FUNCTIONS # # # #
    
    
# WRITE TESTS FOR THIS FUNCTION WITH DIFFERENT INITIAL FOLDERS # 
def findBackUps(current_dir):
    # reinitialise
    files_found = []
    # back ups could be called database_name or tmpfile_name depending
    # on when the program last cut out
    print("Files found in current directory: " +str(os.listdir(current_dir)))
    # find current directory and form tmp file path
    tmp_path = current_dir + "\\" + "tmp.txt"
    # find if it exists
    dbs = [file for file in os.listdir(current_dir) if database_name in file]
    print("dbs = %s"%(dbs))
    tmps = [file for file in os.listdir(current_dir) if tmpfile_name in file]
    print("tmps = %s"%(tmps))
    if len(dbs) == 0 and len(tmps) == 0:
        print("No databases or temp files found from last session")
        files_found = []
    if len(dbs) == 1 and len(tmps) == 0:
        print("One database and no temp files found - last database action completed successfully")
        files_found =  [dbs[0]]
    if len(dbs) == 1 and len(tmps) == 1:
        print("One database and one temp file found - last database action disrupted")
        # likely that the database is corrupted and the tmp file is fine
        files_found = [dbs[0],tmps[0]]
        #recovered = False
    if len(dbs) == 0 and len(tmps) == 1:
        # likely the program was terminated during an addObject() or deleteObject() function
        files_found = [tmps[0]]
    else:
        pass
    
    print("Returning: %s" %(files_found))
    return files_found

def checkIfCorrupt(to_check):
    # assume incoming file is un-corrupt
    corrupt_status = False
    with open(to_check,'rb') as check_file:
        # while there are chars to read
        #while True:
           for line in check_file:
               try:
                   line.decode("ascii")
               except UnicodeDecodeError:
                   print("BAD LINE: " + str(line))
                   corrupt_status = True
               else:
                   print("GOOD LINE")
                   print(line)
                   # no non-ascii chars found - continue reading
                   pass
    return corrupt_status

def checkBackUps(files_found):
    # check the files files_found[0] = database and files_found[1] = tmp_file
    print("Checking for back ups")
    # no databases or temp files found - indicates new session
    if len(files_found) == 0:
        # start afresh
        corrupt_status = "new session"
    if len(files_found) == 1:
        db_check = files_found[0]
        print("Saved database found - checking if %s is corrupt" %(db_check))
        # if exists, check for non-ASCII characters (corruption)
        corrupt_status = checkIfCorrupt(db_check)
        # if true, delete the file
        # if false, as if user wants to continue with the recovered file
    if len(files_found) == 2:
        corrupt_status = True
        # possible mid-action termination
        if checkIfCorrupt(files_found[0]) == True and checkIfCorrupt(files_found[1]) == False:
            # database corrupted but tmp file OK
            corrupt_status = "mid action"
            
    return corrupt_status


    
def initDatabase(corrupt_status):
    print("initialising database based on corrupt status: %s" %(corrupt_status))
    # if no back-ups found start from scratch
    if corrupt_status == True or corrupt_status == "new session":
        print("No existing / valid recovered files found")
        # no valid database or temp file found - delete if exists invalidly
        # delete any files that might exist
        deleteOld()
        # create new files
        createNew()
            
    elif corrupt_status == False: # non-corrupted DATABASE found
        print("Proceed with recovered database? (Y/N)")
        response = input()
        # act on response
        if response == "Y":
            # continue appending database and logfile
            print("Proceeding with recovered database") # what if no log file found?
            # add message to logfile saying when file was recovered
            updateLog(None,getTime(),getDate(),"recover")
        elif response == "N":
            deleteOld()
            createNew()  
        else:
            print("Please enter a valid Y/N response")
     
    elif corrupt_status == "mid action":
        # this indicates a corrupt database but valid temp file
        # delete database but retain tempfile - rename tmpfile as database
        os.remove(database_name)
        os.rename(tmpfile_name,database_name)
        # now we are starting with just a VALID database and no tmpfile
    else:
        print("Invalid corrupted stats - CHECK THIS IMMEDIATELY")


        
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