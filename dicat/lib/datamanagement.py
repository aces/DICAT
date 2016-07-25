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
    """
    Parses the XML file and return the data into xmldoc.

    :param: xmlfile

    :return: xmldoc
     :rtype: object

    """

    try:
        xmldoc = minidom.parse(xmlfile)
        return xmldoc

    except:
        message = "ERROR: could not read file " + xmlfile
        print message #TODO: create a log class to display the messages

def read_data(xmlfile):
    """

    :param xmlfile: XML file to read to grep the data
     :type xmlfile: str

    :return xmldata: everthing that is available under the data tag in the XML
     :rtype xmldata: object
    :return xmlcandlist: list of candidates
     :rtype xmlcandlist: list

    """

    global xmldoc

    xmldoc      = read_xmlfile(xmlfile)
    xmldata     = xmldoc.getElementsByTagName('data')[0]
    xmlcandlist = xmldata.getElementsByTagName('Candidate')

    return xmldata, xmlcandlist

def read_candidate_data():
    """
    Read and return the candidate level content of an XML file specified in the
    global variable Config.xmlfile. Returns an empty dictionary nothing if file
    doesn't exist.

    :param: None

    :return: data
     :rtype: dict

    """

    data = {}
    # check to see if file exists before loading it
    if os.path.isfile(Config.xmlfile):
        # read the xml file
        (xmldata, xmlcandlist) = read_data(Config.xmlfile)
        for cand in xmlcandlist:
            data[cand] = {}
            for elem in cand.childNodes:
                tag = elem.localName
                if not tag or tag == "Visit":
                    continue
                val = cand.getElementsByTagName(tag)[0].firstChild.nodeValue
                data[cand][tag] = val
    else:
        data = ""

    return data


def save_candidate_data(cand_data):
    """
    Save the updated candidate information into the xml file (defined by the
    global variable Config.xmlfile).

    :param cand_data: data dictionary with the updated information
     :type cand_data: dict

    :return: None

    """

    # check to see if xmldoc global variable and file exist before saving
    if os.path.isfile(Config.xmlfile) and xmldoc:
        # read the xml file
        (xmldata, xmlcandlist) = read_data(Config.xmlfile)
        updated = False
        for cand in xmlcandlist:
            for elem in cand.childNodes:
                tag = elem.localName
                if not tag:
                    continue
                val = cand.getElementsByTagName(tag)[0].firstChild.nodeValue
                if tag == "Identifier" and val == cand_data['Identifier']:
                    xml_firstname = cand.getElementsByTagName("FirstName")[0]
                    xml_lastname  = cand.getElementsByTagName("LastName")[0]
                    xml_gender = cand.getElementsByTagName("Gender")[0]
                    xml_dob    = cand.getElementsByTagName("DateOfBirth")[0]
                    xml_phone  = cand.getElementsByTagName("PhoneNumber")[0]
                    xml_status = cand.getElementsByTagName("CandidateStatus")[0]

                    xml_firstname.firstChild.nodeValue = cand_data['FirstName']
                    xml_lastname.firstChild.nodeValue  = cand_data['LastName']
                    xml_gender.firstChild.nodeValue = cand_data['Gender']
                    xml_dob.firstChild.nodeValue    = cand_data['DateOfBirth']
                    xml_status.firstChild.nodeValue = cand_data['CandidateStatus']
                    xml_phone.firstChild.nodeValue  = cand_data['PhoneNumber']

                    updated = True
                    break

        # if no candidate was updated, insert a new candidate
        if not updated:
            # Create a new Candidate element
            cand = xmldoc.createElement("Candidate")
            xmldata.appendChild(cand)

            for key in cand_data:
                xml_elem = xmldoc.createElement(key)
                cand.appendChild(xml_elem)
                txt = xmldoc.createTextNode( cand_data[key] )
                xml_elem.appendChild(txt)

        # update the xml file with the correct values
        f = open(Config.xmlfile, "w")
        xmldoc.writexml(f, addindent="  ", newl="\n")
        f.close()
        # remove the empty lines inserted by writexml
        remove_empty_lines_from_file(Config.xmlfile)

def read_visitset_data():
    """
    Read and return the visit set content of an XML file specified in the
    global variable Config.xmlfile. Returns an empty dictionary nothing if
    file doesn't exist.

    :param: None

    :return: data
     :rtype: dict

    """

    data = {}
    #check to see if file exists before loading it
    if os.path.isfile(Config.xmlfile):
        # read the xml file
        (xmldata, xmlcandlist) = read_data(Config.xmlfile)
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
    """
    Read the visit data related to a specific candidate and update the data
    dictionary.

    :param xmlvisitlist: list of visits to loop through
     :type xmlvisitlist: list
    :param cand: candidate key
     :type cand: object
    :param data: data dictionary containing all candidate and visit's data
     :type data: dict

    :return: None

    """

    data[cand]["VisitSet"] = {}
    for visit in xmlvisitlist:
        data[cand]["VisitSet"][visit] = {}
        for visit_elem in visit.childNodes:
            visit_tag = visit_elem.localName
            if not visit_tag:
                continue
            visit_val = visit.getElementsByTagName(visit_tag)[0].firstChild.nodeValue
            data[cand]["VisitSet"][visit][visit_tag] = visit_val


def read_study_data():
    """Read and return the content of a file called studydata. Returns nothing if file doesn't exist"""
    #check to see if file exists before loading it
    if os.path.isfile("studydata"):
        #load file
        db = pickle.load(open("studydata", "rb"))
    else:
        db = ""
    return db


def save_study_data(data):
    """Save data in a pickle file named studydata.
    Will overwrite any existing file.  Will create one if it doesn't exist"""
    pickle.dump(data, open("studydata", "wb"))


def remove_empty_lines_from_file(file):
    """
    This function allows to remove empty lines that are inserted by writexml
    function from minidom.

    :param file: file that need empty lines to be removed
     :type file: str
    """

    # grep all lines that are not empty into lines
    with open(file) as f:
        lines = [line for line in f if line.strip() is not ""]
    # write lines into the file
    with open(file, "w") as f:
        f.writelines(lines)

#self-test "module"  TODO remove
if __name__ == '__main__':
    print 'testing module:  datamanagement.py'
    data=dict(read_visitset_data("../new_data_test.xml"));
    print data;
