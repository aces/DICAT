#!/usr/bin/env python

#import standard packages
from Tkinter import *
from ttk import *
#import internal packages
import ui.datatable as DataTable
import ui.datawindow as DataWindow
import lib.multilanguage as MultiLanguage
import lib.config as Config


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

        ## Plot the button action in the pane frame

        # Candidate pane frame buttons
        self.buttonNewCandidate = Button(
            self.candidate_pane,
            width=12,
            text=MultiLanguage.candidate_add,
            command=self.add_candidate
        )
        self.buttonNewCandidate.pack(side=TOP, anchor=W)

        ## Create data tables (using Treeview)

        # Candidate datatable
        candidate_column_headers = (
            'identifier', 'firstname', 'lastname', 'date of birth',
            'gender',     'phone',     'status'
        )
        self.cand_table = DataTable.ParticipantsList(
            self.candidate_pane, candidate_column_headers
        )
        self.cand_table.pack(side=BOTTOM, expand=YES, fill=BOTH)

        # Calendar datatable
        visit_column_headers = (
            'identifier', 'candidate', 'visitlabel', 'when', 'where', 'status'
        )
        self.visit_table = DataTable.VisitList(
            self.visit_pane, visit_column_headers
        )
        self.visit_table.pack(side=BOTTOM, expand=YES, fill=BOTH)

        #TODO This section to be replaced by REAL CODE actively filtering data
        """
        #Create a filter section in each data_pane (not implemented yet)


        self.filter_candidate = Labelframe(
            self.candidate_pane, text='Filters', width=220, height=50,
            borderwidth=10
        )
        self.filter_candidate.pack(side=TOP, expand=NO, fill=BOTH, pady=5)
        self.filter_candidate_label = Label(
            self.filter_candidate,
            text='Filter for Non-Active / Active / Excluded / Group...'
        )
        self.filter_candidate_label.pack(side=TOP, expand=NO, fill=BOTH)
        self.filter_visit = Labelframe(
            self.visit_pane, text='Filters', width=220, height=50,
            borderwidth=10
        )
        self.filter_visit.pack(side=TOP, expand=NO, fill=BOTH, pady=5)
        self.filter_candidate_label = Label(
            self.filter_visit,
            text='Filters for Active / Tentative / Closed ...'
        )
        self.filter_candidate_label.pack(side=TOP, expand=NO, fill=BOTH)
        """


    def add_candidate(self):
        """
        This function will allow functionality to add a new candidate using
        the same data window as when editing a subject.

        """

        # Open the datawindow
        DataWindow.DataWindow(self, "new")

        # Update the candidate datatable when save the new candidate
        self.cand_table.update_data()

    def LoadXML(self):
        """
        Update candidate and calendar/visit datatables with data extracted from
        XML file stored in Config.xmlfile.

        """

        # Load XML data into candidate datatable
        self.cand_table.update_data()

        # Load XML data into visit datatable
        self.visit_table.update_data()