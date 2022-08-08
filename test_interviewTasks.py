# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 11:06:18 2022

@author: ellie
"""

# which functions do I want to test?
# 1) findBackUps()
    # a. Test file is found when one exists
    # b. Test no file is found when one doesn't exist
    
    
    # def findBackUps():
        # find current directory and form tmp file path


import unittest
import IBMTasks
import DB_manage

# contains no files
dummy_emp_folder = "C:\\Users\\ellie\\OneDrive\\FreeYear\\IBM Testing Environment\\TestEnv1_empty"

# contains corrupted database but valid temp file
dummy_rec_folder = "C:\\Users\\ellie\\OneDrive\\FreeYear\\IBM Testing Environment\\TestEnv2_recovered"
valid_tmp = "C:\\Users\\ellie\\OneDrive\\FreeYear\\IBM Testing Environment\\TestEnv2_recovered\\tmp.txt"

# technically this one shouldn't happen
dummy_cor_folder = "C:\\Users\\ellie\\OneDrive\\FreeYear\\IBM Testing Environment\\TestEnv3_corrupted"
invalid_tmp = "C:\\Users\\ellie\\OneDrive\\FreeYear\\IBM Testing Environment\\TestEnv3_corrupted\\tmp.txt"

class TestIBMTasks(unittest.TestCase):
    
    def test_add(self):
        result = IBMTasks.add(5,5)
        self.assertEqual(result,10)
    

# =============================================================================
# def findBackUps(current_dir):
#     # back ups could be called database_name or tmpfile_name depending
#     # on when the program last cut out
#     print("Files found in current directory: %s" %(os.listdir(current_dir)))
#     # find current directory and form tmp file path
#     tmp_path = current_dir + "\\" + "tmp.txt"
#     # find if it exists
#     dbs = [file for file in os.listdir(current_dir) if database_name in file]
#     tmps = [file for file in os.listdir(current_dir) if tmpfile_name in file]
#     if len(dbs) == 0 and len(tmps) == 0:
#         print("No databases or temp files found from last session")
#         files_found = []
#     if len(dbs) == 1 and len(tmps) == 0:
#         print("One database and no temp files found - last database action completed successfully")
#         files_found =  [dbs[0]]
#     elif len(dbs) == 1 and len(tmps) == 1:
#         print("One database and one temp file found - last database action disrupted")
#         # likely that the database is corrupted and the tmp file is fine
#         files_found = [dbs[0],tmps[0]]
#         #recovered = False
#     
#     return files_found
# =============================================================================

    def test_findBackUps(self):
        # test cases to handle different types of recovery files
        
        # test empty env 
        files_found = DB_manage.findBackUps(dummy_emp_folder)
        print(files_found)
        # should not find any file
        self.assertEqual(len(files_found), 0, msg = "Correct: no files found")
        
        print("RUNNING NEXT TEST")
        
        # test recovered env
        files_found = DB_manage.findBackUps(dummy_rec_folder)
        # should find temp file
        self.assertEqual(len(files_found), 2 , msg="Correct: Two files found")
        
        print("RUNNING NEXT TEST")
        
        # test corrupted env
        files_found = DB_manage.findBackUps(dummy_cor_folder)
        # should not find temp file
        #print(files_found)
        self.assertEqual(len(files_found), 1, msg = "Correct: One file found")
        
    
        
        
    def test_checkIfCorrupt(self):
        # test cases to handle different types of files
        
        # check non-corrupt file
        corrupt_status = DB_manage.checkIfCorrupt(valid_tmp)
        self.assertFalse(corrupt_status, msg = "Expects non-corrupt file")
        
        print("RUNNING NEXT TEST")
        
        # check corrupt file
        corrupt_status = DB_manage.checkIfCorrupt(invalid_tmp)
        self.assertTrue(corrupt_status, msg = "Expects corrupt file")
        
if __name__ == '__main__':
    unittest.main()
    
        
        