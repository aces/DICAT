#!/usr/bin/python

import ttk
from Tkinter import *

from dicom_anonymizer_frame import dicom_deidentifier_frame_gui
from IDMapper import IDMapper_frame_gui
from welcome_frame import welcome_frame_gui

class DicAT_application():

    # Constructor of the class DicAT called with a parent widget ("parent")
    # to which we will add a number of child widgets. The constructor starts
    # by creating a "Frame" widget. A frame is a simple container.
    def __init__(self, parent, side=LEFT):

        self.dir_opt = {}

        # Title of the application
        parent.title("DICAT")

        # Use notebook (nb) from ttk from Tkinter to create tabs
        self.nb = ttk.Notebook(parent)

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
        self.nb.add(self.page2, text='DICOM de-identifier')
        self.nb.add(self.page3, text='Scheduler', state='hidden') # hide scheduler for now
        self.nb.add(self.page4, text='ID key')

        # Draw
        self.nb.pack(expand=1, fill='both')

        # Draw content of the different tabs' frame
        self.dicom_deidentifier_tab()
        self.id_key_frame()
        self.welcome_page()

    def dicom_deidentifier_tab(self):

        # start dicom_anonymizer_frame_gui method
        dicom_deidentifier_frame_gui(self.page2)


    def id_key_frame(self):

        # start the ID mapper frame gui
        IDMapper_frame_gui(self.page4)


    def welcome_page(self):

        # start the Welcome page
        welcome_frame_gui(self.page1)



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
