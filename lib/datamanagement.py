#imports from standard packages
import os.path
import pickle
"""
The data_management.py file contains functions related to data management only.
Generic functions: savedata(data, datafilename) and readdata(datafile).  Currently, these are not being used.

Specific functions read_candidate_data(), save_candidate_data(), read_studydata() and save_study_data() are used to get/save candidate data and study setup data respectively.
"""


def read_candidate_data():
    """Read and return the content of a file called candidatedata. Returns nothing if file doesn't exist"""

    #check to see if file exists before loading it
    if os.path.isfile("candidatedata"):
        #load file
        db = pickle.load(open("candidatedata", "rb"))
    else:
        db = ""
    return db


def save_candidate_data(data):
    """Save data in a pickle file named candididatedata.
    Will overwrite any existing file.  Will create one if it doesn't exist"""
    pickle.dump(data, open("candidatedata", "wb"))


def read_studydata():
    """Read and return the content of a file called studydata. Returns nothing if file doesn't exist"""
    #check to see if file exists before loading it
    if os.path.isfile("studydata"):
        #load file
        db = pickle.load(open("studydata", "rb"))
    else:
        db = ""
    return  db


def save_study_data(data):
    """Save data in a pickle file named studydata.
    Will overwrite any existing file.  Will create one if it doesn't exist"""
    pickle.dump(data, open("studydata", "wb"))



#self-test "module"  TODO remove
if __name__ == '__main__':
    print 'testing module:  datamanagement.py'
    data=dict(read_candidate_data());
    print data;
