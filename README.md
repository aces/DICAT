# DicAT (DICOM Anonymization Tool)

With the increasing use of web-based database systems, such as [LORIS](http://www.loris.ca) ([Das *et al.*, 2011](http://journal.frontiersin.org/article/10.3389/fninf.2011.00037/full), [Das *et al.*, 2016](http://www.sciencedirect.com/science/article/pii/S1053811915008009)), for large scale imaging studies, de-identification of DICOM datasets becomes a requirement before they can be uploaded in such databases.

![Flow Chart](images/TypicFlowChartOfDICOMdeidentification.png)
***Typical Flow Chart of DICOM de-identification.*** *Before DICOM datasets can be uploaded into a web-based database, identifying information stored in the DICOM header (e.g. patient name, date of birth...) need to be removed. DicAT produces two archival outputs, one with a back-up of the original DICOM files and one with the de-identified DICOM datasets that can then be uploaded into other systems.* 

DicAT is a simple graphical tool that facilitates DICOM de-identification directly on the workstation with its embedded ID key feature that saves a key with the candidates' real name and identifiers for reference in longitudinal studies. 

This tool, which works on all operating systems and is very light in terms of dependencies, was originaly created during the OHBM 2014 and 2015 Hackathons. 


## How to install and run DicAT

Installation instructions vary depending on the operating systems used. See below for detailed information.

Running DicAT will open a window with three different tabs:

* A simple **"Welcome to DicAT"** tab giving a short description of the tool
* A **"DICOM anonymizer"** tab, in which de-identification of DICOMs will take place 
* An **"ID Key"** tab, containing the key between patient's names and their IDs.

![Welcome page](images/Welcome_DicAT.png)
***Welcome page of DicAT.***

### On UNIX operating systems (Linux and OS X) 

To install DicAT on a computer, download and save the content of the current repository into a workstation.

DicAT can be started by executing `DicAT_application.py` script with a Python compiler. Once in the main directory of DicAT, run the following:

```python DicAT_application.py```

### On Windows operating system

To install DicAT, download the following zip archive `Zip_file_with_Windows_executable.zip` containing the DicAT executable and libraries. Extract the content of the archive onto a workstation.

Once the archive has been extracted, double-clicking on the ==anonymizer_gui.exe== executable will open the application.

## How to use the DICOM anonymizer of DicAT?

#### DICOM anonymizer tab of the application and selection of a directory containing DICOM files

![DICOM anonymizer 1](images/DICOM_anonymizer1.png)
***DICOM anonymizer tab of DicAT.*** *In the "DICOM anonymizer" tab (1), a select button (2) allows to select a directory containing DICOM files to anonymize.*

#### View/edit the DICOM fields and de-identify the DICOM files

![DICOM anonymizer 2](images/DICOM_anonymizer2.png)
***View DICOM fields and anonymize the dataset.*** *Once a directory containing DICOM files have been selected (as described in the above section), the DICOM fields can be viewable when clicking on the “View DICOM fields” button (1). The DICOM fields will be displayed in a table with editable fields in black (2) and non-editable fields greyed out (3). By default, editable fields are “PatientName”, “PatientBirthDate” and “PatientSex”. The “Clear” button (4) will erase values from all editable fields. The non-editable fields will be replaced by empty strings in the DICOM files when running the anonymization, while the editable fields will be replaced by what is being entered by the user. Finally, once the user has finalized the edits, clicking on the “Anonymize” button (5) will run the anonymization tool on the DICOM dataset.*


## How to use the ID Key of DicAT

The ID Key feature of DicAT allows storage of the key between identifiable patient's information (*Real Name* and *Date of Birth*) and study’s identifiers that will be used for de-identification. This information will be kept on the workstation. See the following figure for detailed information on how to use this feature.

![ID Key](images/ID_Mapper.png)
***ID key feature of DicAT.*** *This feature allows storage of the mapping information between patient’s information and study IDs. A candidate can be looked up using the* “Search candidate” *button (2) after having entered either the* “Identifier” *or the* “Real Name” *text fields available in the top row (1). The* “Clear fields” *button (3) allows clearing the text in those text fields. A new candidate can be registered using the* “Add candidate” *button (4) after having entered the* “Identifier”*,* “Real Name” *and* “Date of birth” *information in the text fields of the top row (1). Clicking on a subject row (5) of the table displayed at the bottom of the application will automatically populate the text fields (1) with the information of the candidate. The* “Real Name” *or* “Date of birth” *of that candidate can be edited if needed by altering the field and clicking on the* “Edit candidate” *button (6).*

## Authors

Ayan Sengupta <uam111@gmail.com>              - Concept, DICOM-toolkit implementation, Pydicom implementation   

Cecile Madjar <cecile.madjar@gmail.com>       - GUI implementation, PyDICOM implementation, python integration of DICOM-toolkit

Dave MacFarlane <david.macfarlane2@mcgill.ca> - ID Key

Samir Das <samir.das@mcgill.ca>               - Concept and guidance

Daniel Krötz <d.kroetz@fz-juelich.de>         - Documentation, testing on Windows

Christine Rogers <christine.rogers@mcgill.ca> - Documentation
