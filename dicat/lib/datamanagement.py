#imports from standard packages
import os.path
import pickle
from xml.dom import minidom
import config as Config
"""
The data_management.py file contains functions related to data management only.
Generic functions: savedata(data, datafilename) and readdata(datafile).  Currently, these are not being used.

Specific functions read_candidate_data(), save_candidate_data(), read_studydata() and save_study_data() are used to get/save candidate data and study setup data respectively.
"""

def read_xmlfile(xmlfile):

    """Parses the XML file return the data into xmldoc"""
    try:
        xmldoc = minidom.parse(xmlfile)
        return xmldoc

    except:
        message = "ERROR: could not read file " + xmlfile
        print message #TODO: create a log class to display the messages


def read_candidate_data():
    """Read and return the content of a file called candidatedata. Returns nothing if file doesn't exist"""

    data = {}
    #check to see if file exists before loading it
    if os.path.isfile(Config.xmlfile):
        # read the xml file
        xmldoc      = read_xmlfile(Config.xmlfile)
        xmldata     = xmldoc.getElementsByTagName('data')[0]
        xmlcandlist = xmldata.getElementsByTagName('Candidate')
        for cand in xmlcandlist:
            data[cand] = {}
            for elem in cand.childNodes:
                tag = elem.localName
                if not tag or tag == "Visit":
                    continue
                val = cand.getElementsByTagName(elem.localName)[0].firstChild.nodeValue
                data[cand][tag] = val
    else:
        data = ""

    return data

def read_visitset_data():
    """Read and return the content of a file called candidatedata. Returns nothing if file doesn't exist"""

    data = {}
    #check to see if file exists before loading it
    if os.path.isfile(Config.xmlfile):
        # read the xml file
        xmldoc      = read_xmlfile(Config.xmlfile)
        xmldata     = xmldoc.getElementsByTagName('data')[0]
        xmlcandlist = xmldata.getElementsByTagName('Candidate')
        for cand in xmlcandlist:
            data[cand] = {}
            for cand_elem in cand.childNodes:
                cand_tag = cand_elem.localName
                tags_to_ignore = ( "Gender",      "DateOfBirth",
                                   "PhoneNumber", "CandidateStatus"
                                 )
                if not cand_tag or cand_tag in tags_to_ignore:
                    continue
                if cand_tag == "Visit":
                    xmlvisitlist = cand.getElementsByTagName('Visit')
                    read_visit_data(xmlvisitlist, cand, data)

                val = cand.getElementsByTagName(cand_tag)[0].firstChild.nodeValue
                data[cand][cand_tag] = val
    else:
        data = ""

    return data

def read_visit_data(xmlvisitlist, cand, data):
    data[cand]["VisitSet"] = {}
    for visit in xmlvisitlist:
        data[cand]["VisitSet"][visit] = {}
        for visit_elem in visit.childNodes:
            visit_tag = visit_elem.localName
            if not visit_tag:
                continue
            visit_val = visit.getElementsByTagName(visit_tag)[0].firstChild.nodeValue
            data[cand]["VisitSet"][visit][visit_tag] = visit_val

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
    data=dict(read_visitset_data("../new_data_test.xml"));
    print data;
