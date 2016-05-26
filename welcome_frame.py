#!/usr/bin/python

import Tkinter, Tkconstants, tkFileDialog, tkMessageBox
import os
from Tkinter import *

class welcome_frame_gui(Frame):

    def __init__(self, parent):
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.frame = Frame(self.parent, bg="red")
        self.frame.pack(expand=1, fill='both')

        message = '''
        DicAT is a simple tool for anonymization of DICOM datasets.

        The DICOM anonymizer tab allows you to:
            1) select a DICOM directory
            2) view the DICOM headers information
            3) run the anonymization tool on all DICOMs of the directory

        The ID key tab allows to:
            1) store ID information for a given candidate
            2) look for ID information from a given candidate
        '''
        welcome_message = Label(self.frame,
                                text=message,
                                anchor=NW,
                                justify=LEFT
                               )
        welcome_message.pack(expand=1, fill='both')