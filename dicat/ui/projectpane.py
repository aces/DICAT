# Import from standard packages
from Tkinter import *

# Import from DICAT libraries
import lib.multilanguage as multilanguage

class ProjectPane(LabelFrame):
    """
    This class will contain everything about the Project Pane.

    """

    def __init__(self, parent):
        """
        Initialize the ProjectPane class

        :param parent: frame where to put the project pane
         :type parent: object

        """

        LabelFrame.__init__(self, parent)