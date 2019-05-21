import lib.dicom_anonymizer_methods as methods

import os, sys, getopt

def main():
    csv_file     = ''
    xml_zap_file = None
    verbose      = False
    long_options = ["help", "csvfile=", "xmlfile=", "verbose"]
    usage        = (
        'usage  : mass_deidentify -c <csv_file>\n\n'
        'options: \n'
        '\t-c, --csvfile: path to the CSV file with the following format\n'
        '\t-x, --xmlfile: path to the XML file with the list of DICOM fields to zap\n'
        '\t-v, --verbose: if set, be verbose. Note: regardless of whether the\n'
        '\t               verbose option is set, a summary of success/failure\n'
        '\t               will be provided at the end of execution.\n\n'
        'expected format for the CSV file:\n'
        '\t- one row per DICOM study directory\n'
        '\t- four columns separated by "," in the following order:\n'
        '\t\t<DCM_DIR>,<Pname>,<DoB>,<Sex>\n'
        '\t\t-> DCM_DIR: full path to the DICOM study to deidentify\n'
        '\t\t-> Pname  : new patient name to use for deidentification\n'
        '\t\t-> DOB    : date to use as a date of birth (can be empty string)\n'
        '\t\t-> Sex    : sex of the participant (can be left empty)\n'
        '\t- example of a CSV file with three DICOM studies:\n'
        '\t\t \'/data/John_Doe/\',\'subject_ID_1\',\'1981-01-01\',\'M\'\n'
        '\t\t \'/data/Lana_Bip/\',\'subject_ID_2\',\'\',\'F\'\n'
        '\t\t \'/data/Suzy_Bud/\',\'subject_ID_3\',\'1979-10-10\',\'\'\n\n'
        'examples of XML files can be found in dicat/data directory:\n'
        '\t- fields_to_zap.xml: default DICAT list of fields to zap\n'
        '\t- fields_to_zap.xml: more stringent list of fields to zap that could be\n'
        '\t                     used on imaging data for open science releases\n'
    )

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hx:c:v', long_options)
    except getopt.GetoptError as err:
        print usage
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print usage
            sys.exit()
        elif opt in ("-c", "--csvlist"):
            csv_file = arg
        if opt in ("-x", "--xmlfile"):
            xml_zap_file = arg
        if opt in ("-v", "--verbose"):
            verbose = True

    if xml_zap_file and not os.path.isfile(xml_zap_file):
        message = 'ERROR: Could not find the XML file with the list of DICOM fields to zap'
        print message
        print usage
        sys.exit(2)

    if os.path.isfile(csv_file):
        dicom_dict_list = methods.read_csv(csv_file)
        (success_arr, error_arr, no_valid_dicom) = methods.mass_zapping(
            dicom_dict_list, verbose, xml_zap_file
        )
        methods.print_mass_summary(success_arr, error_arr, no_valid_dicom)
    else:
        message = 'ERROR: you must specify a valid CSV file'
        print message
        print usage
        sys.exit(2)





if __name__ == "__main__":
    main()
