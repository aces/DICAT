import shelve
"""
The data_management.py file contains functions related to data management only.
Generic functions: savedata(data, datafilename) and readdata(datafile)

Specific functions readcandidatedata(), savecandidatedata(), readstudydata() and savestudydata() are used to get/save candidate data and study setup data respectively. 
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
def readcandidatedata():
    db = shelve.open("candidatedata")
    return db


def savecandidatedata(data):
    db = shelve.open("candidatedata")
    for key in data:
        db[data[key].uid] = data[key]
    db.close()


def readstudydata():
    db = shelve.open("studydata")
    return db


def savestudydata(data):
    db = shelve.open("studydata")
    for key in data:
        db[data[key].uid] = data[key]
    db.close()

#self-test "module"  TODO remove
if __name__ == '__main__':
    print 'testing module:  datamanagement.py'
    data=dict(readcandidatedata());
    print data;
