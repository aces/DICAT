# Imports from standard packages
import os.path
from xml.dom import minidom

# Imports from DICAT
import config as Config

"""
This file contains functions related to data management only.

Generic functions:
    - read_data(xmlfile)
    - read_xmlfile(xmlfile)
    - remove_enpty_lines_from_file(file)

Specific functions:
    - read_candidate_data()
    - read_visitset_data()
    - read_visit_data(xmlvisitlist, cand, data)
    - save_candidate_data(cand_data)
    - read_study_data()
    - save_study_data()
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


def grep_list_of_candidate_ids():
    """
    Read the XML file and grep all candidate IDs into an array candIDs_array.

    :return: candIDs_array, or False if could not find the XML file

    """

    candIDs_array = []

    if os.path.isfile(Config.xmlfile):
        # read the xml file
        (xmldata, xmlcandlist) = read_data(Config.xmlfile)

        for cand in xmlcandlist:
            for elem in cand.childNodes:
                tag = elem.localName
                if tag == 'Identifier':
                    cand_elem = cand.getElementsByTagName(tag)[0]
                    candID    = cand_elem.firstChild.nodeValue
                    candIDs_array.append(candID)
    else:
        return False

    return candIDs_array

def save_candidate_data(cand_data):
    """
    Save the updated candidate information into the xml file (defined by the
    global variable Config.xmlfile).

    :param cand_data: data dictionary with the updated information
     :type cand_data: dict

    :return: None

    """

    # Check to see if xmldoc global variable and file exist before saving
    if os.path.isfile(Config.xmlfile) and xmldoc:
        # Read the xml file
        (xmldata, xmlcandlist) = read_data(Config.xmlfile)
        updated = False

        # Loop through all the candidates that exist in the XML file
        for cand in xmlcandlist:
            for elem in cand.childNodes:
                tag = elem.localName
                if not tag:
                    continue
                val = cand.getElementsByTagName(tag)[0].firstChild.nodeValue

                # If the candidate was found in the XML file, updates its info
                if tag == "Identifier" and val == cand_data['Identifier']:

                    # Grep the XML elements
                    xml_firstname = cand.getElementsByTagName("FirstName")[0]
                    xml_lastname  = cand.getElementsByTagName("LastName")[0]
                    xml_gender = cand.getElementsByTagName("Gender")[0]
                    xml_dob    = cand.getElementsByTagName("DateOfBirth")[0]
                    xml_phone  = cand.getElementsByTagName("PhoneNumber")[0]
                    xml_status = cand.getElementsByTagName("CandidateStatus")[0]

                    # Replace elements' value with what has been captured in
                    # the cand_data dictionary
                    xml_firstname.firstChild.nodeValue = cand_data['FirstName']
                    xml_lastname.firstChild.nodeValue  = cand_data['LastName']
                    xml_dob.firstChild.nodeValue = cand_data['DateOfBirth']
                    if 'Gender' in cand_data:
                        print "in cand_data gender"
                        xml_gender.firstChild.nodeValue = cand_data['Gender']
                    if 'CandidateStatus' in cand_data:
                        key = 'CandidateStatus'
                        xml_status.firstChild.nodeValue = cand_data[key]
                    if 'PhoneNumber' in cand_data:
                        key = 'PhoneNumber'
                        xml_phone.firstChild.nodeValue = cand_data[key]

                    updated = True
                    break

        # If no candidate was updated, insert a new candidate
        if not updated:
            # Create a new Candidate element
            cand = xmldoc.createElement("Candidate")
            xmldata.appendChild(cand)

            # Loop through cand_data keys ('Identifier', 'FirstName' ...)
            # and add them to the XML handler (xmldoc)
            for key in cand_data:
                # create the child tag ('Gender', 'DOB' etc...) and its value
                xml_elem = xmldoc.createElement(key)
                value    = xmldoc.createTextNode(cand_data[key])
                # append the child tag and value to the 'Candidate' tag
                cand.appendChild(xml_elem)
                xml_elem.appendChild(value)

            # Loop through optional fields and add them to the XML handler
            # with an empty string if the field was not present in cand_data
            optional_fields = ['Gender', 'CandidateStatus', 'PhoneNumber']
            for key in optional_fields:
                if key not in cand_data:
                    # create the new tag and its value
                    xml_elem = xmldoc.createElement(key)
                    value    = xmldoc.createTextNode(" ")
                    # append the child tag and value to the 'Candidate' tag
                    cand.appendChild(xml_elem)
                    xml_elem.appendChild(value)

        # Update the xml file with the correct values
        f = open(Config.xmlfile, "w")
        xmldoc.writexml(f, addindent="  ", newl="\n")
        f.close()
        # Remove the empty lines inserted by writexml (weird bug from writexml)
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

    data = {} # Initialize data dictionary

    # Check to see if file exists before loading it
    if os.path.isfile(Config.xmlfile):
        # Read the xml file
        (xmldata, xmlcandlist) = read_data(Config.xmlfile)

        # Loop through all candidates present in the XML file
        for cand in xmlcandlist:
            data[cand] = {}
            for cand_elem in cand.childNodes:
                cand_tag = cand_elem.localName
                tags_to_ignore = (
                    "Gender", "DateOfBirth", "PhoneNumber", "CandidateStatus"
                )

                # Continue if met a non-wanted tag
                if not cand_tag or cand_tag in tags_to_ignore:
                    continue

                # If the tag is 'Visit', grep all visit information.
                # This will be stored in data[cand]['VisitSet'] dictionary
                if cand_tag == "Visit":
                    xmlvisitlist = cand.getElementsByTagName('Visit')
                    read_visit_data(xmlvisitlist, cand, data)

                # This will store candidate information (such as 'Identifier',
                # 'Gender', 'Firstname' ...) into data[cand][cand_tag].
                elem = cand.getElementsByTagName(cand_tag)[0]
                val  = elem.firstChild.nodeValue
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

    data[cand]["VisitSet"] = {} # Initialize a VisitSet dictionary

    # Loop through all visits present in the XML file for a given candidate
    for visit in xmlvisitlist:
        data[cand]["VisitSet"][visit] = {} # Initialize a Visit dictionary

        # Loop through all visit elements present under a given Visit tag
        for visit_elem in visit.childNodes:
            visit_tag = visit_elem.localName

            if not visit_tag: # continue if no tag
                continue

            # Insert the visit tag and its value into the visit dictionary
            elem = visit.getElementsByTagName(visit_tag)[0]
            val  = elem.firstChild.nodeValue
            data[cand]["VisitSet"][visit][visit_tag] = val


def read_study_data(): #TODO: implement this function
    """
    This function reads and returns the content of the XML 'projectInfo' tag.
    It will return nothing if it could not find the information.

    :return:

    """
    #check to see if file exists before loading it
    pass


def save_study_data(study_data): #TODO: implement this function
    """
    Save study/project information into the XML file under the tag 'projectInfo'

    :param study_data: dictionary containing all the study/project information
     :type study_data: dict

    :return:
    """
    pass


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


