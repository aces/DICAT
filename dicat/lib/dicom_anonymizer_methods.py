import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import re
import shutil
import csv
import lib.resource_path_methods as PathMethods

"""
Test whether PyDICOM module exists and import it.
Notes:
  - in the past, PyDICOM was imported using "import pydicom as dicom"
  - newer versions of the PyDICOM module are imported using "import dicom"
  - returns true if the PyDICOM was imported, false otherwise
"""
# Create a boolean variable that returns True if PyDICOM was imported, False
# otherwise
use_pydicom = False
try:
    import pydicom as dicom

    use_pydicom = True  # set to true as PyDICOM was found and imported
except ImportError:
    try:  # try importing older versions of PyDICOM
        import dicom

        use_pydicom = True  # set to true as PyDICOM was found and imported
    except ImportError:
        use_pydicom = False  # set to false as PyDICOM was not found

if use_pydicom:
    from pydicom.errors import InvalidDicomError

def find_deidentifier_tool():
    """
    Determine if the PyDICOM python module is present and imported.

    :param: None

    :return: True if PyDICOM was found, False otherwise
     :rtype: bool

    """

    if use_pydicom:
        return True
    else:
        return False


def grep_dicoms_from_folder(dicom_folder):
    """
    Grep recursively all DICOMs from folder

    :param dicom_folder: folder to look for DICOMs
     :type dicom_folder: str

    :returns:
      dicoms_list  -> list of DICOMs (with full path)
      subdirs_list -> list of subdirectories (with full path)
     :rtype: list

    """

    # Initialize list of DICOMs and subdirectories
    dicoms_list  = []
    subdirs_list = []
    # Grep DICOM files recursively and insert them in dicoms_list
    # Same for subdirectories
    for root, subdirs, files in os.walk(dicom_folder, topdown=True):
        if len(files) != 0 or len(subdirs) != 0:
            thisdir = re.sub(dicom_folder, '', root)
            if thisdir != '' and thisdir not in subdirs_list:
                subdirs_list.append(thisdir)
            for dicom_file in files:
                if is_file_a_dicom(root + "/" + dicom_file):
                    dicoms_list.append(os.path.join(root, dicom_file))
        else:
            continue

    return dicoms_list, subdirs_list


def is_file_a_dicom(file):
    """
    Check whether a given file is of type DICOM

    :param file: path to the file to identify
     :type file: str

    :return: True if the file is DICOM, False otherwise
     :rtype: bool

    """

    try:
        dicom.read_file(file)
    except InvalidDicomError:
        return False
    return True




def grep_dicom_fields(xml_file):
    """
    Read DICOM fields from XML file called "fields_to_zap.xml"

    :param xml_file: XML file to read
     :type xml_file: str

    :return: dicom_fields -> dictionary of DICOM fields
     :rtype: dict
    """

    xmldoc = ET.parse(xml_file)
    dicom_fields = {}
    for item in xmldoc.findall('item'):
        dicom_tag = item.find('name').text
        description = item.find('description').text
        editable = True if (item.find('editable').text == "yes") else False
        dicom_fields[dicom_tag] = {
            "DICOM_tag"  : dicom_tag,
            "Description": description,
            "Editable"   : editable
        }

    return dicom_fields


def grep_dicom_values(dicom_folder, dicom_fields):
    """
    Grep the value from the different DICOM fields.

    :param dicom_folder: folder with DICOMs
     :type dicom_folder: str
    :param dicom_fields: dictionary of DICOM fields
     :type dicom_fields: dict

    :return: updated dictionary of DICOM fields with DICOM values
     :rtype: dict

    """

    # Grep list of DICOMs in the directory (validation that the list of files
    # are DICOMs happened during grep_dicoms_from_folder)
    (dicoms_list, subdirs_list) = grep_dicoms_from_folder(dicom_folder)

    # If no DICOM files were found, return false
    if not dicoms_list:
        return []

    # Grep the first DICOM to read field information
    dicom_file = dicoms_list[0]

    # Read DICOM file using PyDICOM
    (dicom_fields) = read_dicom_with_pydicom(dicom_file, dicom_fields)

    return dicom_fields


def read_dicom_with_pydicom(dicom_file, dicom_fields):
    """
    Read DICOM file using PyDICOM python library.

    :param dicom_file: DICOM file to read
     :type dicom_file: str
    :param dicom_fields: Dictionary containing DICOM fields and values
     :type dicom_fields: dict

    :return: updated dictionary of DICOM fields and values
     :rtype : dict

    """

    # Read DICOM file
    dicom_dataset = dicom.read_file(dicom_file)

    # Grep information from DICOM header and store them
    # into dicom_fields dictionary under flag Value
    # Dictionnary of DICOM values to be returned
    for name in dicom_fields:
        try:
            description = dicom_fields[name]['Description']
            value = dicom_dataset.data_element(description).value
            dicom_fields[name]['Value'] = value
        except:
            continue

    return dicom_fields


def dicom_zapping(dicom_folder, dicom_fields):
    """
    Zap DICOM fields using PyDICOM recursive wrapper

    :param dicom_folder: folder with DICOMs
     :type dicom_folder: str
    :param dicom_fields: dictionary of DICOM fields and values
     :type dicom_fields: dict

    :returns:
      deidentified_zip -> path to the zip file of the de-identified DICOMs
      original_zip  -> path to the zip file of the original DICOMs
     :rtype: str

    """

    # Grep all DICOMs present in directory
    (dicoms_list, subdirs_list) = grep_dicoms_from_folder(dicom_folder)

    # Create an original_dcm and deidentified_dcm directory in the DICOM folder,
    # as well as subdirectories
    (original_dir, deidentified_dir) = create_directories(dicom_folder,
                                                      dicom_fields,
                                                      subdirs_list)

    # Move DICOMs into the original_directory created and copy DICOMs into the
    # deidentified_folder
    for dicom in dicoms_list:
        if not len(dicom):
            continue
        # set path to de-identified DICOM file
        deidentified_dcm = dicom.replace(dicom_folder, deidentified_dir)
        # set path to original DICOM file
        original_dcm = dicom.replace(dicom_folder, original_dir)
        # Move DICOM files from root folder to de-identified folder created
        shutil.move(dicom, deidentified_dcm)
        # copy files from original folder to de-identified folder
        shutil.copy(deidentified_dcm, original_dcm)
        # Zap the DICOM fields from DICOM file using PyDICOM
        pydicom_zapping(deidentified_dcm, dicom_fields)

    # Zip the de-identified and original DICOM folders
    (deidentified_zip, original_zip) = zip_dicom_directories(deidentified_dir,
                                                             original_dir,
                                                             subdirs_list,
                                                             dicom_folder
                                                            )

    # return zip files
    return deidentified_zip, original_zip


def pydicom_zapping(dicom_file, dicom_fields):
    """
    Actual zapping method for PyDICOM

    :param dicom_file: DICOM to de-identify
     :type dicom_file: str
    :param dicom_fields: Dictionary with DICOM fields & values to use
     :type dicom_fields: dict

    :return: None

    """

    dicom_dataset = dicom.read_file(dicom_file)

    for name in dicom_fields:
        new_val = ""
        if 'Value' in dicom_fields[name]:
            new_val = dicom_fields[name]['Value'].strip()

        if dicom_fields[name]['Editable'] is True:
            try:
                dicom_dataset.data_element(
                    dicom_fields[name]['Description']).value = new_val
            except:
                continue
        else:
            try:
                dicom_dataset.data_element(
                    dicom_fields[name]['Description']).value = ''
            except:
                continue
    dicom_dataset.save_as(dicom_file)


def zip_dicom_directories(deidentified_dir, original_dir, subdirs_list, root_dir):
    """
    Zip the de-identified and origin DICOM directories.

    :param deidentified_dir: directory with the de-identified DICOM files
     :type deidentified_dir: str
    :param original_dir: directory with the original DICOM files
     :type original_dir: str
    :param subdirs_list: list of subdirectories within the DICOM directories
     :type subdirs_list: list
    :param root_dir: root directory of the zip files to be created
     :type root_dir: str

    :returns:
      deidentified_zip -> path to the zip file of the de-identified DICOM files
      original_zip  -> path to the zip file of the original DICOM files
     :rtype: str

    """


    # If de-identified and original folders exist, zip them
    if os.path.exists(deidentified_dir) and os.path.exists(original_dir):
        original_zip = zip_dicom(original_dir)
        deidentified_zip = zip_dicom(deidentified_dir)
    else:
        sys.exit('Failed to find original and de-identify data folders')

    # If archive de-identified and original DICOMs found, remove subdirectories in
    # root directory
    if os.path.exists(deidentified_zip) and os.path.exists(original_zip):
        for subdir in subdirs_list:
            if os.path.exists(root_dir + os.path.sep + subdir):
                shutil.rmtree(root_dir + os.path.sep + subdir)
    else:
        sys.exit('Failed: could not zip de-identified and original data folders')

    # Return zip files
    return deidentified_zip, original_zip


def create_directories(dicom_folder, dicom_fields, subdirs_list):
    """
    Create two directories in the main DICOM folder:
        - one to copy over the original DICOM sub-folders and files
        - one for the de-identified DICOM dataset

    :param dicom_folder: path to the folder containing the DICOM dataset
     :type dicom_folder: str
    :param dicom_fields: dictionary of DICOM fields and values
     :type dicom_fields: dict
    :param subdirs_list: list of subdirectories found in dicom_folder
     :type subdirs_list: list

    :returns:
      original_dir     -> directory containing original DICOM dataset
      deidentified_dir -> directory containing de-identified DICOM dataset
     :rtype: str

    """

    # Create an original_dcm and deidentified_dcm directory in the DICOM folder,
    # as well as subdirectories
    patient_name     = dicom_fields['0010,0010']['Value'].strip()
    original_dir     = dicom_folder + os.path.sep + patient_name
    deidentified_dir = dicom_folder + os.path.sep + patient_name + "_deidentified"
    os.mkdir(original_dir, 0755)
    os.mkdir(deidentified_dir, 0755)
    # Create subdirectories in original and de-identified directory, as found in
    # DICOM folder
    for subdir in subdirs_list:
        os.mkdir(original_dir + os.path.sep + subdir, 0755)
        os.mkdir(deidentified_dir + os.path.sep + subdir, 0755)

    return original_dir, deidentified_dir


def zip_dicom(directory):
    """
    Function that zip a directory.

    :param directory: path to the directory to zip
     :type directory: str

    :return: archive -> path to the created zip file
     :rtype: str

    """

    archive = directory + '.zip'

    if (os.listdir(directory) == []):
        sys.exit(
            "The directory " + directory + " is empty and will not be zipped.")
    else:
        shutil.make_archive(directory, 'zip', directory)

    if (os.path.exists(archive)):
        shutil.rmtree(directory)
        return archive
    else:
        sys.exit(archive + " could not be created.")


def read_csv(csv_file):
    """
    Function that reads a CSV file and return its content in an list of
    dictionaries.
        - Each row in the CSV will be one entry in the list.
        - Each column {names : values} for a given row will be stored in a
        dictionary within that row.

    Example of a row in the returned array:
    {'dcm_dir': '/path/to/dicom/dir', 'pname': 'sub-01', 'dob': '', 'sex': 'M'}

    :param csv_file: CSV file to be read
     :type csv_file: str

    :return: dicom_dict_list -> list of dictionaries with 1 row per DICOM study
     :rtype: list

    """

    fieldnames = ['dcm_dir', 'pname', 'dob', 'sex']
    dicom_dict_list   = []
    with open(csv_file) as file:
        reader = csv.DictReader(file, fieldnames, restval='')

        for row in reader:
            dicom_dict_list.append(row)

    return dicom_dict_list


def mass_zapping(dicom_dict_list, verbose, xml_file_with_fields_to_zap):
    """
    Function that deidentifies a given list of DICOM studies.

    :param dicom_dict_list: list of dictionaries with 1 row per DICOM study.
                            See description of read_csv() above to see
                            dictionary's structure
     :type dicom_dict_list: list
         
    :returns:
      success_arr -> list of DICOM studies successfully deidentified
      error_arr   -> list of DICOM studies not properly deidentified
     :rtype: list

    """

    success_arr    = []
    error_arr      = []
    no_valid_dicom = []
    for row in dicom_dict_list:
        field_dict = map_DICOM_fields(row, xml_file_with_fields_to_zap)
        if not field_dict:
            print 'No valid DICOM file was found in ' + row['dcm_dir']
            no_valid_dicom.append(row['dcm_dir'])
            continue
        if verbose:
            print 'Deidentifying DICOM study: ' + row['dcm_dir']

        # get rid of '\ ' in DICOM path and map it to ' ' for the zapping method
        dicom_dir = row['dcm_dir'].replace('\ ', ' ')
        (deidentified_dcm, original_dcm) = dicom_zapping(
            dicom_dir, field_dict
        )

        # check if deidentification was successful
        if os.path.exists(deidentified_dcm) != [] and os.path.exists(
                original_dcm) != []:
            success_arr.append(row['dcm_dir'])
        else:
            error_arr.append(row['dcm_dir'])

    return success_arr, error_arr, no_valid_dicom


def map_DICOM_fields(dicom_dict, xml_file_with_fields_to_zap):
    """
    Function that maps DICOM values with the new values provided in dicom_dict.

    :param dicom_dict: DICOM dictionary with DICOM path, new patient name, dob
                       and sex information to modify into the DICOM files
     :type dicom_dict: dict
    :param xml_file_with_fields_to_zap: path to the XML file with the list of
                                        DICOM fields to zap
     :type xml_file_with_fields_to_zap: str


    :return: field_dict -> dictionary of {field: values} to be replaced in DICOM
     :rtype: dict

    """

    # Read the XML file with the identifying DICOM fields
    if xml_file_with_fields_to_zap is None:
        xml_file = load_xml('data/fields_to_zap.xml')
    else:
        xml_file = xml_file_with_fields_to_zap
    field_dict = grep_dicom_fields(xml_file)

    # Read DICOM header and grep identifying DICOM field values
    dicom_dir  = dicom_dict['dcm_dir'].replace('\ ', ' ')  # get rid of '\ '
    field_dict = grep_dicom_values(dicom_dir, field_dict)

    if not field_dict:
        return []

    for key in field_dict.keys():
        if field_dict[key]['Editable'] == False:
            continue
        if field_dict[key]['Description'] == 'PatientName':
            update_DICOM_value(field_dict, key, dicom_dict['pname'])
        elif field_dict[key]['Description'] == 'PatientBirthDate':
            update_DICOM_value(field_dict, key, dicom_dict['dob'])
        elif field_dict[key]['Description'] == 'PatientSex':
            update_DICOM_value(field_dict, key, dicom_dict['sex'])

    return field_dict


def update_DICOM_value(field_dict, key, value):
    """
    Function that updates a DICOM value stored in field_dict with the new value
    provided as input. This new value will be modified later on in the DICOMs.

    :param field_dict: dictionary with DICOM fields and values
     :type field_dict: dict
    :param key       : key of the DICOM field to update
     :type key       : str
    :param value     : new value to insert into the DICOM files
     :type value     : str

    """

    if 'Value' in field_dict[key]:
        if field_dict[key]['Value'] == value:
            field_dict[key]['Update'] = False
        else:
            field_dict[key]['Value']  = value
            field_dict[key]['Update'] = True
    else:
        field_dict[key]['Update'] = False


def load_xml(xml_path):
    """
    Function that determines the full path to the XML file

    :param xml_path: path to the XML file (could be a relative path)
     :type xml_path: str

    :return: XML_file -> full path to the XML file to be read if it exists  in
             the filesystem, None otherwise
     :rtype: str

    """

    # Read the XML file with the identifying DICOM fields
    load_xml = PathMethods.resource_path(xml_path)
    XML_filename = load_xml.return_path()

    if os.path.isfile(XML_filename):
        XML_file = XML_filename
    else:
        XML_filepath = os.path.dirname(os.path.abspath(__file__))
        XML_file = XML_filepath + "/" + XML_filename

    return XML_file if os.path.isfile(XML_file) else None


def print_mass_summary(success_list, error_list, no_valid_dicom):
    """
    Function that prints out a summary of the successfully deidentified DICOM
    studies and the not propoerly deidentified DICOM studies.

    :param success_list  : list of DICOM studies successfully deidentified
     :type success_list  : list
    :param error_list    : list of DICOM studies not properly deidentified
     :type error_list    : list
    :param no_valid_dicom: list of DICOM studies with no valid DICOM files
     :type no_valid_dicom: list

    """

    if success_list:
        # print the successful cases
        print "\nList of successfully deidentified datasets:"
        print "\t" + "\n\t".join(str(success) for success in success_list) + "\n"
    else:
        print "\nNo datasets were successfully deidentified.\n"

    if no_valid_dicom:
        # print the cases where no DICOM files were found
        print "\nList of datasets with no valid DICOM files found:"
        print "\t" + "\n\t".join(str(invalid) for invalid in no_valid_dicom) + "\n"
    elif error_list:
        # print the other cases where something wrong happened
        print "List of datasets that were not successfully deidentified:"
        print "\t" + "\n\t".join(str(error) for error in error_list) + "\n"
    else:
        print "\nAll datasets were successfully deidentified!\n"
