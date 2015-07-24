import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import re
import glob
import platform
import shutil
from shutil import move
import pydicom

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
# Grep value from dicom fields using PyDicom #
################################
def Grep_DICOM_values_PyDicom(dicom_dir, dicom_fields):
    # Grep first dicom of the directory
    # TO DO: Need to check if file is dicom though, otherwise go to next one
    file_list = []
    for f in os.listdir(dicom_dir):
        file_list.append(f)
    dicom_file = dicom_dir + os.path.sep + file_list[0]
    dicom_dataset = dicom.read_file(dicom_file)
    return_dict={}
    # Grep information from dicom header and store them 
    # into dicom_fields dictionary under flag Value
    for field_values in dicom_fields.values():
        #print field_values['Description']
        try:
            print field_values['Description']+'->'+dicom_dataset.data_element(field_values['Description']).value
            return_dict[field_values['Description']]=dicom_dataset.data_element(field_values['Description']).value
        except:
            continue    

    return return_dict



################################
# Grep value from dicom fields #
################################
def Grep_DICOM_values(dicom_dir, dicom_fields):
    # Grep first dicom of the directory
    # TO DO: Need to check if file is dicom though, otherwise go to next one
    file_list = []
    for f in os.listdir(dicom_dir):
        file_list.append(f)
    dicom_file = dicom_dir + os.path.sep + file_list[1]
    
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
# Run dcmmodify on all fields to zap using PyDicom recursive wrapper#
######################################
def Dicom_zapping_PyDicom(dicom_folder, dicom_fields):
    anonymized_folder=dicom_folder+'_anonymized'
    shutil.copytree(dicom_folder, anonymized_folder)

    for root,dirs,files in os.walk(anonymized_folder):
        if len(files)!=0:
            for dicom_file in files:
                print 'anonymizing->'+dicom_file
                actual_zapping(os.path.join(root, dicom_file), dicom_fields)  


######################################
# Actual zapping method #
######################################
def actual_zapping(dicom_file, dicom_fields):
    

    dicom_dataset = dicom.read_file(dicom_file)

    for field_values in dicom_fields.values():
        if field_values['Editable'] is True:
            try:
                dicom_dataset.data_element(field_values['Description']).value=''
                
            except:
                continue
    dicom_dataset.save_as(dicom_file)


######################################
# Run dcmmodify on all fields to zap #
######################################
def Dicom_zapping(dicom_folder, dicom_fields):
    
    # Grep all dicoms present in directory
    file_list = []
    for f in os.listdir(dicom_folder):
        file_list.append(f)

    # Create an original_dcm and anonymized_dcm directory in dicom_folder
    original_dcm = dicom_folder + os.path.sep + "original_dcm"
    anonymize_dcm = dicom_folder + os.path.sep + "anonymized_dcm"
    os.mkdir(original_dcm, 0755)
    os.mkdir(anonymize_dcm, 0755)
    opSystem = platform.system()
    # Move all dicom files into anonymized_dcm (we'll move the .bak file into original_dcm once dcmodify has been run) 
    for f in file_list:
        move(dicom_folder + os.path.sep + f, anonymize_dcm)
         
    # Create the dcmodify command
    # Have to overcome Mac's Argument list is too long error 
    # using UNIX xargs which will not work on default Windows config
    if opSystem == 'Windows':
        modify_cmd = "dcmodify "
    else:
        modify_cmd = "echo "

    changed_fields_nb = 0
    for name in dicom_fields:
        # Grep the new values
        new_val = ""
        if 'Value' in dicom_fields[name]: 
            new_val = dicom_fields[name]['Value']

        # Run dcmodify if update is set to True
        if not dicom_fields[name]['Editable'] and 'Value' in dicom_fields[name]: #kr#
            modify_cmd += " -ma \"(" + name + ")\"=\" \" " #kr#
            print modify_cmd
            changed_fields_nb += 1
        else:
            if dicom_fields[name]['Update'] == True:
                modify_cmd += " -ma \"(" + name + ")\"=\"" + new_val + "\" "
                print modify_cmd
                changed_fields_nb += 1
    modify_cmd += anonymize_dcm + os.path.sep + "*"
   
    # If no dicom field was updated
    if changed_fields_nb > 0:
        if opSystem == 'Windows': 
            subprocess.call(modify_cmd, shell=True)
        else:
            subprocess.call(modify_cmd + " |xargs dcmodify", shell=True)
        globuleux = anonymize_dcm + os.path.sep + "*.bak" 
        for bak_file in glob.glob(globuleux):
            first = bak_file.rfind(os.path.sep)
            last = bak_file.find(".bak")
            new_name = bak_file[first:last]
            move(bak_file, original_dcm + new_name)            
    else:
        move(anonymize_dcm + os.path.sep + "*", original_dcm)
        
    return anonymize_dcm, original_dcm

### Test function
def anonymize_folder(folder_name):
    print folder_name
    dict_data_fields={'Name':'Ayan','Age':25}
    if not os.path.exists(folder_name):
        sys.exit('The directory selected does not exist....')
    else:
        return dict_data_fields
        
