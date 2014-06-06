import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import re

###################################
# Read dicom fields from XML file #
###################################
def Grep_DICOM_fields(xml_file):
    xmldoc = ET.parse(xml_file)
    dicom_fields = {}
    for item in xmldoc.findall('item'):
        name = item.find('name').text
        description = item.find('description').text
        dicom_fields[name] = {"Description": description}
    return dicom_fields




################################
# Grep value from dicom fields #
################################
def Grep_DICOM_values(dicom_dir, dicom_fields):
    # Grep first dicom of the directory
    # TO DO: Need to check if file is dicom though, otherwise go to next one
    find_cmd = "find " + dicom_dir + " -type f "
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
    for name in dicom_fields:
        print name
        value = ""
        if 'Update' in dicom_fields[name]:
            update = dicom_fields[name]['Update']
        modify_cmd = "dcmodify -ma (" + name + ")=\"" + value + "\""
        print modify_cmd





### Test function
def anonymize_folder(folder_name):
    print folder_name
    dict_data_fields={'Name':'Ayan','Age':25}
    if not os.path.exists(folder_name):
        sys.exit('The directory selected does not exist....')
    else:
        return dict_data_fields
        
