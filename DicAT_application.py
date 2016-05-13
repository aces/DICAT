#!/usr/bin/python

import ttk
from Tkinter import *

from dicom_anonymizer_frame import dicom_anonymizer_frame_gui
from IDMapper import IDMapper_frame_gui

class DicAT_application():

    # Constructor of the class DicAT called with a parent widget ("master")
    # to which we will add a number of child widgets. The constructor starts
    # by creating a "Frame" widget. A frame is a simple container.
    def __init__(self, master, side=LEFT):

        self.dir_opt = {}

        # Title of the application
        master.title("DicAT")

        # Use notebook (nb) from ttk from Tkinter to create tabs
        self.nb = ttk.Notebook(master)

        # Add frames as pages for ttk.Notebook
        self.page1 = ttk.Frame(self.nb)

        # Second page, DICOM anonymizer
        self.page2 = ttk.Frame(self.nb)

        # Third page, Scheduler
        self.page3 = ttk.Frame(self.nb)

        # Fourth page, ID key
        self.page4 = ttk.Frame(self.nb)

        # Add the pages to the notebook
        self.nb.add(self.page1, text='Welcome to DicAT!')
        self.nb.add(self.page2, text='DICOM anonymizer')
        self.nb.add(self.page3, text='Scheduler', state='hidden') # hide scheduler for now
        self.nb.add(self.page4, text='ID key')

        # Draw
        self.nb.pack(expand=1, fill='both')

        # Draw content of the different tabs' frame
        self.dicom_anonymizer_tab()
        #TODO: create a ID_key_GUI class
        self.id_key_frame()
        self.welcome_page()

    #TODO: have header window display within the application, not a TopLevel window
    def dicom_anonymizer_tab(self):

        # start dicom_anonymizer_frame_gui method
        dicom_anonymizer_frame_gui(self.page2)


    def id_key_frame(self):
        print "ID key in function"

        # start the ID mapper frame gui
        IDMapper_frame_gui(self.page4)

    def welcome_page(self):

        message = '''
        DicAT is a simple tool for anonymization of DICOM datasets.

        The DICOM anonymizer tab allows you to:
            1) select a DICOM directory
            2) view the DICOM headers information
            3) run the anonymization tool on all DICOMs of the directory

        The ID key tab allows to:
            1) store ID information for a given participant/patient
            2) look for ID information from a given participant/patient
        '''
        welcome_message = Label(self.page1,
                                text=message,
                                anchor=NW,
                                justify=LEFT
                               )
        welcome_message.pack(expand=1, fill='both')



if __name__ == "__main__":

    # Create a Tk root widget.
    root = Tk()

    app = DicAT_application(root)

    # The window won't appear until we've entered the Tkinter event loop.
    # The program will stay in the event loop until we close the window.
    root.mainloop()

    # Some development environments won't terminate the Python process unless it is
    # explicitly mentioned to destroy the main window when the loop is terminated.
#    root.destroy()