import lib.dicom_anonymizer_methods as methods

import os, sys, getopt

def main():
    csv_file = ''
    usage    = (
        'usage : mass_deidentify -c <csv_file>\n\n'
        'option: -c, --csvfile: CSV file with the following format\n\n'
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
        '\t\t \'/data/Suzy_Bud/\',\'subject_ID_3\',\'1979-10-10\',\'\'\n'
    )
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:', ["help", "csvfile="])
    except getopt.GetoptError as err:
        print usage
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt in ("-c", "--csvlist"):
            csv_file = arg

    if os.path.isfile(csv_file):
        csv_dict = methods.read_csv(csv_file)
        (success_arr, error_arr) = methods.mass_zapping(csv_dict)
        methods.print_mass_summary(success_arr, error_arr)
    else:
        message = 'ERROR: you must specify a valid CSV file'
        print message
        print usage
        sys.exit(2)





if __name__ == "__main__":
    main()