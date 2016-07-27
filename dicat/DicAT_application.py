#!/usr/bin/python

# Import from standard packages
import ttk
from Tkinter import *

# Import DICAT libraries
from dicom_anonymizer_frame import dicom_deidentifier_frame_gui
from IDMapper import IDMapper_frame_gui
from scheduler_application import UserInterface
from welcome_frame import welcome_frame_gui
import ui.menubar as MenuBar



class DicAT_application():


    def __init__(self, master, side=LEFT):
        """
        Constructor of the class DICAT called with a parent widget ("master")
        to which we will add a number of child widgets. The constructor starts
        by creating a "Frame" widget. A frame is a simple container.

        :param master:
         :type master: object
        :param side:
         :type side:

        """

        self.dir_opt = {}

        # Title of the application
        master.title("DICAT")

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
        self.nb.add(self.page1, text='Welcome to DICAT!')
        self.nb.add(self.page2, text='DICOM de-identifier')
        self.nb.add(self.page3, text='Scheduler')
        self.nb.add(self.page4, text='ID key')

        # Draw
        self.nb.pack(expand=1, fill='both')

        # Draw content of the different tabs' frame
        self.dicom_deidentifier_tab()
        self.id_key_frame()
        self.welcome_page()
        self.scheduler_page(master)


    def dicom_deidentifier_tab(self):
        """
        Start the DICOM de-identifier frame.

        """

        # start dicom_anonymizer_frame_gui method
        dicom_deidentifier_frame_gui(self.page2)


    def id_key_frame(self):
        """
        Start the ID Mapper frame.

        """

        # start the ID mapper frame gui
        IDMapper_frame_gui(self.page4)


    def welcome_page(self):
        """
        Start the Welcome frame.

        """

        # start the Welcome page
        welcome_frame_gui(self.page1)

    def scheduler_page(self, master):
        """
        Start the scheduler frame.

        :param master:
         :type master:
        """

        # initialize the menu bar and start the scheduler frame
        menu = MenuBar.SchedulerMenuBar(master)
        master.config(menu=menu)
        UserInterface(self.page3)

if __name__ == "__main__":

    # Create a Tk root widget.
    root = Tk()

    app = DicAT_application(root)

    # The window won't appear until we've entered the Tkinter event loop.
    # The program will stay in the event loop until we close the window.
    root.mainloop()

    # Some development environments won't terminate the Python process unless
    # it is explicitly mentioned to destroy the main window when the loop is
    # terminated.
#    root.destroy()
