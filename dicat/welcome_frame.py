#!/usr/bin/python

from Tkinter import *

'''
lib.resource_path_methods has been created for Pyinstaller.
Need to load images or external files using these methods, otherwise the
created application would not find them.
'''
import lib.resource_path_methods as PathMethods

class welcome_frame_gui(Frame):

    def __init__(self, parent):
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.frame = Frame(self.parent)
        self.frame.pack(expand=1, fill='both')


        # Insert DICAT logo on the right side of the screen
        load_img = PathMethods.resource_path("images/DICAT_logo.gif")
        imgPath  = load_img.return_path()
        logo     = PhotoImage(file = imgPath)
        logo_image = Label(self.frame,
                           image = logo,
                           bg='white'
                          )
        logo_image.image = logo

        logo_image.pack(side='left', fill='both')

        # Create the Welcome to DICAT text variable
        text   = Text(self.frame, padx=40, wrap='word')
        scroll = Scrollbar(self.frame, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.tag_configure('title',
                           font=('Verdana', 20, 'bold', 'italic'),
                           justify='center'
                          )
        text.tag_configure('bold',    font=('Verdana', 12, 'bold'))
        text.tag_configure('default', font=('Verdana', 12))

        # Insert title into the text variable
        title = "\nWelcome to DICAT!\n\n"
        text.insert(END, title, 'title')

        # Insert introduction of the tool into the text variable
        intro  = "DICAT 2.2 (DICOM Anonymization Tool) is a simple tool for "
        intro += "de-identification of DICOM datasets. In addition to "
        intro += "de-identifying DICOM files, this tool contains a feature "
        intro += "that allows mapping the candidate's information to its "
        intro += "study identifier.\n"
        text.insert(END, intro, 'default')

        # Insert explanation of the DICOM anonymizer tab into the text variable
        tab1 = "\n\nThe DICOM de-identifier tab allows to:\n"
        text.insert(END, tab1, 'bold')

        anonymizer  = '''
        1) select a DICOM directory
        2) view the DICOM headers information
        3) edit or clear the DICOM headers information directly in the table
        4) run the de-identifier tool on all DICOMs of the selected directory with the edited information
        '''
        text.insert(END, anonymizer, 'default')

        # Insert explanation of the ID key tab into the text variable
        tab2 = "\n\nThe ID key tab allows to:\n"
        text.insert(END, tab2, 'bold')

        IDkey = '''
        1) store ID information for a given candidate
        2) look for ID information from a given candidate
        '''
        text.insert(END, IDkey, 'default')

        # Display the text variable
        text.pack(side='left', fill='both', expand=1)
        scroll.pack(side="right", fill='y')
        # Disable the edit functionality of the displayed text
        text.config(state='disabled')
