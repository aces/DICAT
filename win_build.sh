#!/bin/bash
# Script to create Windows executable from anonymizer python scripts
# Make sure the following are installed on your system:
# - Python.  Get Python from http://www.python.org/download/ and install on your machine.
# - py2exe. Get py2exe from  http://www.py2exe.org/
# - pydicom:  python package for working with DICOM files. https://github.com/darcymason/pydicom
# - DCMtk: http://dicom.offis.de/dcmtk.php.en

echo "This will create a Windows executable from Python scripts!"

# creates windows executable from python files
python setup.py py2exe

# copy fields_to_zap.xml to same dir (dist/) as exe file
cp fields_to_zap.xml dist/fields_to_zap.xml
