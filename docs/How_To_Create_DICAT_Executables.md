# How to create DICAT executables

Here is described the procedure used to create DICAT executables for Window, Mac OS X and Linux workstation. In order to be able to follow the steps mentioned below, you will need to install [Pyinstaller](http://www.pyinstaller.org).

## 1) Run pyinstaller on DICAT.py

In the terminal/console, go into the `dicat` directory hosting the DICAT.py script and run the following command depending on the OS used.

### On Mac OS X

```pyinstaller --onefile --windowed --icon=images/DICAT_logo_icns DICAT.py```

### On Windows

```pyinstaller --onefile --windowed --icon=images\dicat_logo_HsB_2.ico DICAT.py```

### On Linux (tested on Ubuntu)

```pyinstaller --onefile DICAT.py```

Executing this command will create a `DICAT.spec` file in the same directory, as well as a `build` and `dist` directory. 

## 2) Edit DICAT.spec

Edit the `DICAT.spec` file to include the path to the image and the XML file used by the application (a.k.a. `images/DICAT_logo.gif` and `data/fields_to_zap.xml`). 

To do so, insert the following lines after the `Analysis` block of the spec file (Note, the /PATH/TO/DICOM_anonymizer should be updated with the proper full path).

```
a.datas += [
    ( 'images/DICAT_logo.gif', 
      '/PATH/TO/DICOM_anonymizer/dicat/images/DICAT_logo.gif', 
      'DATA'
    ),
    ( 'data/fields_to_zap.xml', 
      '/PATH/TO/DICOM_anonymizer/dicat/data/fields_to_zap.xml', 
      'DATA'
    )
]
```

FYI, the analysis block of the spec file looks like:

```
a = Analysis(['DICAT.py'],
             pathex=['/PATH/TO/DICOM_anonymizer/dicat'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
```

## 3) Rerun pyinstaller using DICAT.spec

Once the path to the images have been added, rerun the pyinstaller command on the spec file as follows.

### On Mac OS X

```pyinstaller --onefile --windowed --icon=images/DICAT_logo_icns DICAT.spec```

A `DICAT.app` will be located in the dist directory created by the pyinstaller command. 

To include the DICAT logo to the app, execute the following steps:

1.  Copy the icon to the clipboard
  *  Click on the `DICAT_logo_icns` file from the Finder
  *  Choose 'Get Info' from the 'File' menu.
  *  In the info window that pops up, click on the icon
  *  Choose 'Copy' from the 'Edit' menu.
  *  Close the info window

2.  Paste the icon to the `DICAT.app` item
  *  Go to the `DICAT.app` item in the Finder 
  *  Click on the `DICAT.app` item  
  *  Choose 'Get Info' from the 'File' menu.
  *  In the info window that pops up, click on the icon
  *  Choose 'Paste' from the 'Edit' menu.
  *  Close the info window

Congratulations! You just created the DICAT app for Mac OS X!!

### On Windows

Note: Make sure the paths in the spec file contains \\ instead of \.

```pyinstaller --onefile --windowed --icon=images\dicat_logo_HsB_2.ico DICAT.spec```

A `DICAT.exe` will be located in the dist directory created by the pyinstaller command. 

Congratulations! You just created the DICAT executable for Windows!!

### On Linux (tested on Ubuntu)

```pyinstaller --onefile DICAT.spec```

To include the DICAT logo to the application, execute the following steps:

1. Right click on the application and select "Properties"
2. Double click on the icon on the left
3. Select the DICAT_logo.gif file as the icon

Congratulations! You just created the DICAT application for Linux!!



DICAT