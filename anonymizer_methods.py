import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import re
import glob
import platform
import errno
from shutil import move

# hard coded path or Tom
dcmpath = "/Volumes/botteron/Imaging/Software/DCMTK/dcmtk-3.6.0-mac-i686-dynamic/bin/"

###################################
# Read dicom fields from XML file #
###################################
def Grep_DICOM_fields(xml_file):
    xmldoc = ET.parse(xml_file)
    dicom_fields = {}
    for item in xmldoc.findall('item'):
        name = item.find('name').text
        description = item.find('description').text
        editable = True if (item.find('editable').text=="yes") else False #kr#
        dicom_fields[name] = {"Description": description, "Editable": editable} #kr#
        #dicom_fields[name] = {"Description": description}
    return dicom_fields




################################
# Grep value from dicom fields #
################################
def Grep_DICOM_values(dicom_dir, dicom_fields):
    # Grep first dicom of the directory
    # TO DO: Need to check if file is dicom though, otherwise go to next one
    file_list = []
    for dirname, dirnames, filenames in os.walk(dicom_dir):
        for filename in filenames:
            dicom_file = os.path.join(dirname, filename)
            break
	
    
    # Grep information from dicom header and store them 
    # into dicom_fields dictionary under flag Value
    for name in dicom_fields:
        dump_cmd = dcmpath + "dcmdump -ml +P " + name + " -q " + dicom_file
        result = subprocess.check_output(dump_cmd, shell=True)
        tmp_val = re.match(".+\[(.+)\].+", result)
        if tmp_val:
            value = tmp_val.group(1)
            dicom_fields[name]['Value'] = value
    return dicom_fields



######################################
# Run dcmmodify on all fields to zap #
######################################
def Dicom_zapping(dicom_folder, dicom_fields):

    # get file and directory list
    list_file = []
    for f in os.listdir(dicom_folder):
        list_file.append(f)

    # create new location for files and directories
    anonymize_dcm = os.path.join(dicom_folder, "anonymized_dcm")
    os.mkdir(anonymize_dcm, 0755)

    original_dcm = os.path.join(dicom_folder, "original_dcm")
    os.mkdir(original_dcm, 0755)

    # move all data into anonymized_dcm
    for f in list_file:
        move(os.path.join(dicom_folder, f), anonymize_dcm)

    # Create the dcmodify command
    # Have to overcome Mac's Argument list is too long error 
    # using UNIX xargs which will not work on default Windows config
    if platform.system() == 'Windows':
        modify_cmd = dcmpath + "dcmodify "
        cmd_flag = ""
    else:
        modify_cmd = "echo "
        cmd_flag = " |xargs " + dcmpath + "dcmodify"

    # find the fields to update
    changed_fields_nb = 0
    for name in dicom_fields:

        # Grep the new values
        new_val = ""
        if 'Value' in dicom_fields[name]: 
            new_val = dicom_fields[name]['Value']

        # Run dcmodify if update is set to True
        if not dicom_fields[name]['Editable'] and 'Value' in dicom_fields[name]: #kr#
            modify_cmd += " -ma \"(" + name + ")\"=\" \" " #kr#
            changed_fields_nb += 1
        else:
            if dicom_fields[name]['Update'] == True:
                modify_cmd += " -ma \"(" + name + ")\"=\"" + new_val + "\" "
                changed_fields_nb += 1

    # update files if fields need updating.  otherwise move everything to original
    if changed_fields_nb > 0:

	    # Need to run for each subfolder separately.
        # Also need to ignore directories from file list.
        for dirCurr_anon, subDirs, filenames in os.walk(anonymize_dcm):
            if filenames:
                # create subdirectoreis in original_dcm
                dirRel = os.path.relpath(dirCurr_anon, anonymize_dcm)
                dirCurr_orig = os.path.join(original_dcm, dirRel)
                try:
                    os.makedirs(dirCurr_orig, 0755)
                except OSError as exc:
                    if exc.errno == errno.EEXIST and os.path.isdir(dirCurr_orig):
                        pass
                    else: raise

                # update dicom fields in the files
                for f in filenames:
                    ff = os.path.join(dirCurr_anon, f)
                    subprocess.call(modify_cmd + ff + cmd_flag, shell=True)

                # move and rename bak files to original; assuming no dir names *.bak
                globuleux = os.path.join(dirCurr_anon, "*.bak")
                for fileBak in glob.glob(globuleux):
                    fileNew = re.sub('\.bak','', os.path.basename(fileBak))
                    move(fileBak, os.path.join(dirCurr_orig, fileNew))
    else:
        for f in os.listdir(anonymize_dcm):
            move(os.path.join(anonymize_dcm, f), original_dcm)
        
    return anonymize_dcm, original_dcm

### Test function
def anonymize_folder(folder_name):
    print folder_name
    dict_data_fields={'Name':'Ayan','Age':25}
    if not os.path.exists(folder_name):
        sys.exit('The directory selected does not exist....')
    else:
        return dict_data_fields
        
