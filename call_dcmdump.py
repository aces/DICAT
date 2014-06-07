import xml.etree.ElementTree as ET
import subprocess
import re

##################################################
# Set files - This should be coming from the GUI #
##################################################
dcm_file = "DICOM_test/MR.1.3.12.2.1107.5.2.32.35442.2014041514472688464444623"
XML_file = "fields_to_zap.xml"
dcm_folder = "DICOM_test"

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
def Grep_DICOM_values(dicom_file, dicom_fields):
    for name in dicom_fields:
        dump_cmd = "dcmdump -ml +P " + name + " -q " + dicom_file
        result = subprocess.check_output(dump_cmd, shell=True)
        tmp_val = re.match(".+\[(.+)\].+", result)
        if tmp_val:
            value = tmp_val.group(1)
            dicom_fields[name] = {"Value": value}
    return dicom_fields


######################################
# Run dcmmodify on all fields to zap #
######################################
def Dicom_zapping(dicom_folder, dicom_fields):
    modify_cmd = "dcmodify "
    for name in dicom_fields:
        print name
        value = ""
        if 'Update' in dicom_fields[name]:
            update = dicom_fields[name]['Update']
            modify_cmd += "-ma \"(" + name + ")\"=\"" + value + "\" "
    modify_cmd +=  dicom_folder + "/*"    
    subprocess.call(modify_cmd, shell=True)
    print modify_cmd



test = Grep_DICOM_fields(XML_file)
test2 = Grep_DICOM_values(dcm_file,test)
Dicom_zapping(dcm_folder, test2)
