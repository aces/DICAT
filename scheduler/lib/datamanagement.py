#imports from standard packages
import shelve
import sqlite3
"""
The data_management.py file contains functions related to data management only.
Generic functions: savedata(data, datafilename) and readdata(datafile).  Currently, these are not being used.

Specific functions read_candidate_data(), save_candidate_data(), read_studydata() and save_study_data() are used to get/save candidate data and study setup data respectively.
"""
"""
#Generic functions
def savedata(data, datafilename):
    db = shelve.open(datafilename)
    for key in data:
        db[data[key].uid] = data[key]
    db.close()


def readdata(datafile):
    db = shelve.open(datafile)  #TODO check is db.close() is needed (may be automatic)
    return db
"""

#Specific functions
def read_candidate_data():
    db = shelve.open("candidatedata")
    return db

def save_candidate_data(data):
    db = shelve.open("candidatedata")
    for key in data:
        db[data[key].uid] = data[key]
    db.close()

def read_studydata():
    db = shelve.open("studydata")
    return db

def save_study_data(data):
    db = shelve.open("studydata")
    for key in data:
        db[data[key].uid] = data[key]
    db.close()

#self-test "module"  TODO remove
if __name__ == '__main__':
    print 'testing module:  datamanagement.py'
    data=dict(read_candidate_data());
    print data;
