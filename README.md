# DICAT (DICOM Anonymization Tool)

DICAT is a simple graphical tool that facilitates DICOM (Digital Imaging and Communications in Medicine) de-identification directly on a local workstation.
It works on all major operating systems (Windows, Linux and OSX) and is very light in terms of dependencies.

With the increasing use of web-based database systems, such as [LORIS](http://www.loris.ca) ([Das *et al.*, 2011](http://journal.frontiersin.org/article/10.3389/fninf.2011.00037/full), [Das *et al.*, 2016](http://www.sciencedirect.com/science/article/pii/S1053811915008009)), for large scale imaging studies, de-identification of DICOM datasets becomes a requirement before they can be uploaded in such databases.

![Flow Chart](dicat/images/TypicFlowChartOfDICOMdeidentification.png)

***Typical Flow Chart of DICOM de-identification.***

Before DICOM datasets can be uploaded into a web-based database, identifying information stored in the DICOM header (such as patient name, date of birth) should be removed.

DICAT produces two archival outputs: a back-up of the original DICOM files, and a de-identified DICOM dataset that can then be uploaded or transferred to other systems.

DICAT also features an ID key log that can be used to keep a record of the original candidate name (participant/patient) linked to their anonymized study identifier, for reference by study coordinators. 

DICAT was first developed during the [2014 and 2015 brainhacks](http://brainhack.org) held at the [Organization of Human Brain Mapping (OHBM)](http://www.humanbrainmapping.org/i4a/pages/index.cfm?pageid=1) conferences.

## How to install and run DICAT

Installation instructions vary depending on the operating system used. See below for detailed information.

Running DICAT will open a window with three different tabs:

* A simple **"Welcome to DICAT"** tab giving a short description of the tool
* A **"DICOM de-identifier"** tab, in which de-identification of DICOMs will take place 
* An **"ID Key"** tab, containing the key between candidate's names and their IDs.

![Welcome page](DICAT/images/Welcome_DICAT.png)

***Welcome page of DICAT.***

### On UNIX operating systems (Linux and OS X) 

To install DICAT on a computer, download and save the content of the current repository into a workstation.

DICAT can be started by executing `DICAT_application.py` script with a Python compiler. Once in the main directory of DICAT, run the following:

```python DICAT_application.py```

### On Windows operating system

==To install DICAT, download the following zip archive `Zip_file_with_Windows_executable.zip` containing the DICAT executable and libraries. Extract the content of the archive onto a workstation.==

Once the archive has been extracted, double-clicking on the ==anonymizer_gui.exe== executable will open the application.

## How to use the DICOM de-identifier of DICAT?



![DICOM deidentifier 1](dicat/images/DICOM_deidentification.png)

***DICOM de-identification with DICAT.*** 

In the *"DICOM de-identifier"* tab (1), use the select button (2) to choose a directory containing DICOM files to de-identify.

Once a directory containing DICOM files have been selected (as described in the above section), the DICOM fields can be viewed when clicking on the *“View DICOM fields”* button (3).

 The DICOM fields will be displayed in a table with editable fields in black (4) and non-editable fields greyed out (5). The non-editable fields will be replaced by empty strings in the DICOM files when running the de-identification, while the editable fields will be replaced by the value entered by the user. By default, editable fields are *“PatientName”*, *“PatientBirthDate”* and *“PatientSex”*. ==Mention how to configure editable fields== 
 
The *“Clear”* button (6) will erase values from all editable fields. 

Finally, once the user has finalized the edits, clicking on the *“De-identify”* button (7) will run the de-identification tool on the DICOM dataset. 


## How to use the ID Key of DICAT

The ID Key feature of DICAT allows storage of the key between identifiable candidates's information (*Real Name* and *Date of Birth*) and its study’s identifier. This information will be stored locally on the workstation within an XML file (candidate.xml) in DICAT's directory. See the following figure for detailed information on how to use this feature.

![ID Key](dicat/images/ID_Mapper.png)

***ID key feature of DICAT.*** 

This feature (1) allows storage of the mapping information between candidates’s information and study IDs. This information will be stored in an XML file that can be either created (2) or opened (3). Changes will be automatically saved. 

A candidate (participant/patient) can be looked up using the *“Search candidate”* button (5) after having entered either the *“Identifier”* or the *“Real Name”* text fields available in (4). 

The *“Clear fields”* button (6) allows clearing the text in those text fields. 

A new candidate can be registered using the *“Add candidate”* button (7) after having entered the *“Identifier”*, *“Real Name”* and *“Date of birth”* information in the text fields of (4). 

Clicking on a subject row (8) of the table displayed at the bottom of the application will automatically populate the text fields (4) with the information of the candidate. 

The *“Real Name”* or *“Date of birth”* of that candidate can be edited if needed by altering the field and clicking on the *“Edit candidate”* button (9). 

Finally, the data table of candidate is sortable by clicking on any of the column headers (10).

## Authors

Ayan Sengupta <uam111@gmail.com>              - Concept, DICOM-toolkit implementation, Pydicom implementation   

Cecile Madjar <cecile.madjar@gmail.com>       - GUI implementation, PyDICOM implementation, python integration of DICOM-toolkit, ID key

Dave MacFarlane <david.macfarlane2@mcgill.ca> - ID Key

Samir Das <samir.das@mcgill.ca>               - Concept and guidance

Daniel Krötz <d.kroetz@fz-juelich.de>         - Documentation, testing on Windows

Christine Rogers <christine.rogers@mcgill.ca> - Documentation

Leigh Evans <evansleigh26@gmail.com> - Video tutorial

Derek Lo <derek.lo@mcgill.ca> - Logo design
