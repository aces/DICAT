# Imports from standard packages
import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import re
import shutil

"""
Test whether PyDICOM module exists and import it.
Notes:
  - in the past, PyDICOM was imported using "import pydicom as dicom"
  - newer versions of the PyDICOM module are imported using "import dicom"
  - returns true if the PyDICOM was imported, false otherwise
"""
# Create a boolean variable (use_pydicom) that returns:
#    - True if PyDICOM was succesfully imported
#    - False otherwise
use_pydicom = False
try:
    import pydicom as dicom
    use_pydicom = True  # set to true as PyDICOM was found and imported
except ImportError:
    try:  # try importing newer versions of PyDICOM
        import dicom
        use_pydicom = True  # set to true as PyDICOM was found and imported
    except ImportError:
        use_pydicom = False  # set to false as PyDICOM was not found


def find_deidentifier_tool():
    """
    Determine which de-identifier tool will be used by the program:
    - PyDICOM python module if found and imported
    - DICOM toolkit if found on the filesystem

    :param: None

    :return: tool to use for DICOM de-identification
     :rtype: object

    """

    if use_pydicom:
        # PyDICOM will be used and returned if PyDICOM was found
        return 'PyDICOM'
    elif test_executable('dcmdump'):
        # DICOM toolkit will be used if dcmdump executable exists
        return 'DICOM_toolkit'
    else:
        # Return False if no tool was found to read and de-identify DICOMs
        return False


def test_executable(executable):
    """
    Test if an executable exists.
    Returns True if executable exists, False if not found.

    :param executable: executable to test
     :type executable: str

    :return: return True if executable was found, False otherwise
     :rtype: bool

    """

    # try running the executable
    try:
        subprocess.call([executable], stdout=open(os.devnull, 'wb'))
        return True
    except OSError:
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
    # Regular expression to identify files that are not DICOM.
    pattern = re.compile(
        "\.bmp$|\.png$|\.zip$|\.txt$|\.jpeg$|\.pdf$|\.DS_Store|\._")
    for root, subdirs, files in os.walk(dicom_folder, topdown=True):
        if len(files) != 0 or len(subdirs) != 0:
            thisdir = re.sub(dicom_folder, '', root)
            if thisdir != '' and thisdir not in subdirs_list:
                subdirs_list.append(thisdir)
            for dicom_file in files:
                if pattern.search(dicom_file) is None:
                    dicoms_list.append(os.path.join(root, dicom_file))
        else:
            sys.exit('Could not find any files in ' + dicom_folder)

    return dicoms_list, subdirs_list


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
        name = item.find('name').text
        description = item.find('description').text
        editable = True if (item.find('editable').text == "yes") else False
        dicom_fields[name] = {"Description": description, "Editable": editable}
        # dicom_fields[name] = {"Description": description}

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

    # Grep first DICOM of the directory
    # TODO: Need to check if file is DICOM though, otherwise go to next file
    (dicoms_list, subdirs_list) = grep_dicoms_from_folder(dicom_folder)
    dicom_file = dicoms_list[0]

    # Read DICOM file using PyDICOM
    if (use_pydicom):
        (dicom_fields) = read_dicom_with_pydicom(dicom_file, dicom_fields)
    else:
        (dicom_fields) = read_dicom_with_dcmdump(dicom_file, dicom_fields)

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


def read_dicom_with_dcmdump(dicom_file, dicom_fields):
    """
    Read DICOM file using dcmdump from the DICOM toolkit.

    :param dicom_file: DICOM file to read
     :type dicom_file: str
    :param dicom_fields: Dictionary containing DICOM fields and values
     :type dicom_fields: dict

    :return: updated dictionary of DICOM fields and values
     :rtype : dict

    """

    # Grep information from DICOM header and store them
    # into dicom_fields dictionary under flag Value
    for name in dicom_fields:
        dump_cmd = "dcmdump -ml +P \"" + name + "\" -q \"" + dicom_file + "\""
        result = subprocess.check_output(dump_cmd, shell=True)
        tmp_val = re.match(".+\[(.+)\].+", result)
        if tmp_val:
            value = tmp_val.group(1)
            dicom_fields[name]['Value'] = value

    return dicom_fields


def dicom_zapping(dicom_folder, dicom_fields):
    """
    Run dcmodify on all fields to zap using PyDICOM recursive wrapper

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
        if use_pydicom:
            # copy files from original folder to de-identified folder
            shutil.copy(deidentified_dcm, original_dcm)
            # Zap the DICOM fields from DICOM file using PyDICOM
            pydicom_zapping(deidentified_dcm, dicom_fields)
        else:
            # Zap the DICOM fields from DICOM file using dcmodify
            dcmodify_zapping(deidentified_dcm, dicom_fields)
            # Grep the .bak files created by dcmdump and move it to original
            # DICOM folder
            orig_bak_dcm = deidentified_dcm + ".bak"
            if os.path.exists(orig_bak_dcm):
                shutil.move(orig_bak_dcm, original_dcm)

    # Zip the de-identified and original DICOM folders
    (deidentified_zip, original_zip) = zip_dcm_directories(deidentified_dir,
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
            new_val = dicom_fields[name]['Value']

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


def dcmodify_zapping(dicom_file, dicom_fields):
    """
    Run dcmodify on all DICOM fields to zap.

    :param dicom_file: DICOM file to zap
     :type dicom_file: str
    :param dicom_fields: dictionary of DICOM fields and values
     :type dicom_fields: dict

    :returns:
      original_zip  -> Path to the zip file containing original DICOM files
      deidentified_zip -> Path to the zip containing the de-identified DICOMs
     :rtype: str

    """

    # Initialize the dcmodify command
    modify_cmd = "dcmodify "
    changed_fields_nb = 0
    for name in dicom_fields:
        # Grep the new values
        new_val = ""
        if 'Value' in dicom_fields[name]:
            new_val = dicom_fields[name]['Value']

        # Run dcmodify if update is set to True
        if not dicom_fields[name]['Editable'] and 'Value' in dicom_fields[name]:
            modify_cmd += " -ma \"(" + name + ")\"=\" \" "
            changed_fields_nb += 1
        else:
            if dicom_fields[name]['Update'] == True:
                modify_cmd += " -ma \"(" + name + ")\"=\"" + new_val + "\" "
                changed_fields_nb += 1
    modify_cmd += " \"" + dicom_file + "\" "
    subprocess.call(modify_cmd, shell=True)


def zip_dcm_directories(deidentified_dir, original_dir, subdirs_list, root_dir):
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
        original_zip     = zip_dicom(original_dir)
        deidentified_zip = zip_dicom(deidentified_dir)
    else:
        sys.exit('Failed to find original and de-identify data folders')

    # If archive de-identified and original DICOMs found, remove subdirectories
    # in root directory
    if os.path.exists(deidentified_zip) and os.path.exists(original_zip):
        for subdir in subdirs_list:
            if os.path.exists(root_dir + os.path.sep + subdir):
                shutil.rmtree(root_dir + os.path.sep + subdir)
    else:
        sys.exit('Failed: could not zip de-identified & original data folders')

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
      original_dir  -> directory containing original DICOM dataset
      deidentified_dir -> directory containing de-identified DICOM dataset
     :rtype: str

    """

    # Create an original_dcm and deidentified_dcm directory in the DICOM folder,
    # as well as subdirectories
    name = dicom_fields['0010,0010']['Value']
    original_dir     = dicom_folder + os.path.sep + name
    deidentified_dir = dicom_folder + os.path.sep + name + "_deidentified"
    os.mkdir(original_dir,     0755)
    os.mkdir(deidentified_dir, 0755)
    # Create subdirectories in original and de-identified directory, as found in
    # DICOM folder
    for subdir in subdirs_list:
        os.mkdir(original_dir     + os.path.sep + subdir, 0755)
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
