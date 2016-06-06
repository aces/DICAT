# How to create DICAT executables

Here is described the procedure used to create DICAT executables for Window, Mac OS X and Linux workstation. In order to be able to follow the steps mentioned below, you will need to install [Pyinstaller](http://www.pyinstaller.org).

## Creation of a Mac OS X app

Go into the `dicat` directory hosting the DICAT_application.py script and run the following.

```pyinstaller --onefile --windowed --icon=images/DICAT_logo.icns DICAT_application.py```

This will create a `DICAT_application.spec` file in the same directory, as well as a `build` and `dist` directory. First, edit the `DICAT_application.spec` file to include the path to the image used by the application (a.k.a. `images/DICAT_logo.gif`). To do so, insert the following line after the Analysis block of the spec file.

```a.datas += [('images/DICAT_logo.gif', '/Users/cmadjar/Sites/DICOM_anonymizer/dicat/images/DICAT_logo.gif', 'DATA')]```

FYI, the analysis block of the spec file looks like:

```
a = Analysis(['DICAT_application.py'],
             pathex=['/Users/cmadjar/Sites/DICOM_anonymizer/dicat'],
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

Once the path to the images have been added, rerun the pyinstaller command on the spec file as follows.

```pyinstaller --onefile --windowed --icon=images/DICAT_logo.icns DICAT_application.spec```

The `DICAT_application.app` created will be located in the dist directory created by the pyinstaller command. To include the DICAT logo to the app, execute the following steps:

1.  Copy the icon to the clipboard
  *  Click on the `DICAT_logo.icns` file from the Finder
  *  Choose 'Get Info' from the 'File' menu.
  *  In the info window that pops up, click on the icon
  *  Choose 'Copy' from the 'Edit' menu.
  *  Close the info window

2.  Paste the icon to the `DICAT_application.app` item
  *  Go to the `DICAT_application.app` item in the Finder 
  *  Click on the `DICAT_application.app` item  
  *  Choose 'Get Info' from the 'File' menu.
  *  In the info window that pops up, click on the icon
  *  Choose 'Paste' from the 'Edit' menu.
  *  Close the info window

Congratulations! You just created the DICAT app for Mac OS X!!

## Creation of Windows executables



## Creation of Linux executables


