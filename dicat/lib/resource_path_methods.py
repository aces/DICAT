#!/usr/bin/python

import os
import sys

class resource_path():

    def __init__(self, relative_path):
        self.relative_path = relative_path

    def return_path(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, self.relative_path)

        return os.path.join(os.path.abspath("."), self.relative_path)