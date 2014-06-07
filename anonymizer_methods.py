import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import re
import glob

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
    for f in os.listdir(dicom_dir):
        file_list.append(f)
    dicom_file = dicom_dir + "/" + file_list[1]
    
    # Grep information from dicom header and store them 
    # into dicom_fields dictionary under flag Value
    for name in dicom_fields:
        dump_cmd = "dcmdump -ml +P " + name + " -q " + dicom_file
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
    
    # Grep all dicoms present in directory
    file_list = []
    for f in os.listdir(dicom_folder):
        file_list.append(f)

    # Create an original_dcm and anonymized_dcm directory in dicom_folder
    original_dcm = dicom_folder + "/original_dcm"
    anonymize_dcm = dicom_folder + "/anonymized_dcm"
    os.mkdir(original_dcm, 0755)
    os.mkdir(anonymize_dcm, 0755)
    
    # Move all dicom files into anonymized_dcm (we'll move the .bak file into original_dcm once dcmodify has been run) 
    for f in file_list:
        move_dicom = "mv " + dicom_folder +"/" + f + " " + anonymize_dcm 
        subprocess.call(move_dicom, shell=True)        
    
    # Create the dcmodify command
    modify_cmd = "dcmodify "
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
    modify_cmd += anonymize_dcm + "/*"
   
    # If no dicom field was updated
    if changed_fields_nb > 0: 
        subprocess.call(modify_cmd, shell=True)
        globuleux = anonymize_dcm + "/*.bak" 
        for bak_file in glob.glob(globuleux):
            new_name = re.sub('.bak','',bak_file)
            new_name = re.sub(anonymize_dcm,'',new_name)
            mv_bak_cmd = "mv " + bak_file + " " + original_dcm + new_name
            subprocess.call(mv_bak_cmd, shell=True)
    else:
        mv_dcm_cmd = "mv " + anonymize_dcm + "/* " + original_dcm
        subprocess.call(mv_dcm_cmd, shell=True)

    return anonymize_dcm, original_dcm

### Test function
def anonymize_folder(folder_name):
    print folder_name
    dict_data_fields={'Name':'Ayan','Age':25}
    if not os.path.exists(folder_name):
        sys.exit('The directory selected does not exist....')
    else:
        return dict_data_fields
        
