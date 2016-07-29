#!/usr/bin/env python

#import standard packages
from Tkinter import *
from ttk import *

#import internal packages
import ui.datatable as DataTable
import ui.datawindow as DataWindow
import lib.multilanguage as MultiLanguage


class UserInterface(Frame):

    def __init__(self, parent):
        """
        Initialize the UserInterface class.

        :param parent: parent widget in which to insert the UserInterface
         :type parent: object

        """

        Frame.__init__(self)
        self.parent = parent
        #self.parent.title(MultiLanguage.app_title)
        self.initialize()


    def initialize(self):
        """
        Creates the paned window with the project information, candidate and
        calendar panes.

        """

        # Initialize frame
        self.frame = Frame(self.parent)
        self.frame.pack(side=TOP, expand=YES, fill=BOTH, padx=10, pady=10)

        #TODO implement button to be able to choose the XML file
        #Config.xmlfile = "new_data_test.xml"

        ## Create the PanedWindow

        # This area (datapane) is one Panedwindow containing 3 Labelframes
        # TODO add dynamic resize
        self.data_pane = Panedwindow(
            self.frame, width=1000, height=500, orient=HORIZONTAL
        )
        self.data_pane.pack(side=RIGHT, expand=YES, fill=BOTH)

        ## Create the 3 LabelFrames that will be part of the PanedWindow

        # Project info pane
        # TODO create class for project info pane
        # TODO add dynamic resize
        self.project_infopane = Labelframe(
            self.data_pane, text=MultiLanguage.project_info_pane, width=250,
            height=350,     borderwidth=10
        )

        # Candidate pane
        # TODO add dynamic resize
        self.candidate_pane = Labelframe(
            self.data_pane, text=MultiLanguage.candidate_pane, width=100,
            height=450, borderwidth=10
        )

        # Visit pane
        # TODO add dynamic resize
        self.visit_pane = Labelframe(
            self.data_pane, text=MultiLanguage.calendar_pane, width=100,
            height=350, borderwidth=10
        )
        self.data_pane.add(self.project_infopane)
        self.data_pane.add(self.candidate_pane)
        self.data_pane.add(self.visit_pane)

        ## Plot the button actions in the candidate pane frame

        # Create a frame that will contain the buttons
        self.buttonBox = Frame(self.candidate_pane)
        self.buttonBox.pack(side=TOP, anchor=W)

        # Create a 'new candidate' button to be added to self.buttonBox
        self.buttonNewCandidate = Button(    # new candidate button widget
            self.buttonBox,
            width=15,
            text=MultiLanguage.candidate_add,
            command=self.add_candidate
        )
        self.labelSearchCandidate = Label(   # search candidate Label widget
            self.buttonBox,
            width=8,
            text=MultiLanguage.candidate_search,
            justify=RIGHT,
            anchor=E
        )
        self.textSearchCandValue  = StringVar()
        self.textSearchCandValue.trace('w', self.find_matching_candidates)
        self.entrySearchCandidate = Entry(   # search candidate entry widget
            self.buttonBox, text=self.textSearchCandValue, width=20,
        )
        # Draw the buttons
        self.buttonNewCandidate.grid(
            row=0, column=0, padx=(0,10), pady=(0,5), sticky=E+W
        )
        self.labelSearchCandidate.grid(
            row=0, column=1, padx=(5,0), pady=(0,5), sticky=E+W
        )
        self.entrySearchCandidate.grid(
            row=0, column=2, padx=(0,0), pady=(0,5), sticky=E+W
        )

        ## Create data tables (using Treeview)

        # Candidate datatable
        candidate_column_headers = [
            'identifier', 'firstname', 'lastname', 'date of birth',
            'gender',     'phone',     'status'
        ]
        self.cand_table = DataTable.ParticipantsList(
            self.candidate_pane, candidate_column_headers
        )
        self.cand_table.pack(side=BOTTOM, expand=YES, fill=BOTH)

        # Calendar datatable
        visit_column_headers = [
            'identifier', 'candidate', 'visitlabel', 'when', 'where', 'status'
        ]
        self.visit_table = DataTable.VisitList(
            self.visit_pane, visit_column_headers
        )
        self.visit_table.pack(side=BOTTOM, expand=YES, fill=BOTH)


    def find_matching_candidates(self, *args):
        """
        Updates data table with matching candidates.

        :param args:
         :type args: list

        """
        pattern = self.textSearchCandValue.get()
        self.cand_table.update_data(pattern)


    def add_candidate(self):
        """
        This function will allow functionality to add a new candidate using
        the same data window as when editing a subject.

        """

        # Open the datawindow with candidate=False as no existing ID associated
        # yet for the new candidate
        DataWindow.DataWindow(self, 'new')

        # Update the candidate datatable when save the new candidate
        self.cand_table.update_data()


    def load_xml(self):
        """
        Update candidate and calendar/visit datatables with data extracted from
        XML file stored in Config.xmlfile.

        """

        # Load XML data into candidate datatable
        self.cand_table.update_data()

        # Load XML data into visit datatable
        self.visit_table.update_data()