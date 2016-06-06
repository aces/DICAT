__author__ = 'Karolina Marasinska' 

from distutils.core import setup
import py2exe

setup(
    windows=[
        {
            "script": 'DICAT_application.py',
            "icon_ressources": [(0, "images\dicat_logo_HsB_2.ico")]
	}
    ],
    data_files=[
        ( 
            'images', 
            ['C:\\Users\\Daniel\\Desktop\\Cecile_DICAT\\DICOM_anonymizer\\dicat\\images\\DICAT_logo.gif']
        ),
        (   
            'data',
            ['C:\\Users\\Daniel\\Desktop\\Cecile_DICAT\\DICOM_anonymizer\\dicat\\data\\fields_to_zap.xml']
        )
    ],
  
)