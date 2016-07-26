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
        Frame.__init__(self)
        self.parent = parent
        #self.parent.title(MultiLanguage.app_title)
        self.initialize()

    def initialize(self):

        # initialize frame
        self.frame = Frame(self.parent)
        self.frame.pack(side=TOP, expand=YES, fill=BOTH, padx=10, pady=10)

        #TODO implement button to be able to choose the XML file
        Config.xmlfile = "new_data_test.xml"

        # This area (datapane) is one Panedwindow containing 3 Labelframes
        self.data_pane = Panedwindow( self.frame, width=1000,
                                      height=500, orient=HORIZONTAL
                                    )  # TODO add dynamic resize
        self.data_pane.pack(side=RIGHT, expand=YES, fill=BOTH)
        # TODO create class for project info pane
        self.project_infopane = Labelframe(self.data_pane,
                                           text=MultiLanguage.project_info_pane,
                                           width=250,
                                           height=350,
                                           borderwidth=10
                                          )  # TODO add dynamic resize
        self.candidate_pane = Labelframe( self.data_pane,
                                          text=MultiLanguage.candidate_pane,
                                          width=100,
                                          height=450,
                                          borderwidth=10
                                        )  # TODO add dynamic resize
        self.visit_pane = Labelframe( self.data_pane,
                                      text=MultiLanguage.calendar_pane,
                                      width=100,
                                      height=350,
                                      borderwidth=10
                                    )  # TODO add dynamic resize
        self.data_pane.add(self.project_infopane)
        self.data_pane.add(self.candidate_pane)
        self.data_pane.add(self.visit_pane)

        # plot the button action in the pane frame
        # candidate pane frame buttons
        self.buttonNewCandidate = Button( self.candidate_pane,
                                          width=12,
                                          text=MultiLanguage.candidate_add,
                                          command=self.add_candidate
                                        )
        self.buttonNewCandidate.pack(side=TOP, anchor=W)

        # create data tables (treeview)
        # candidate table
        candidate_column_headers = (
            'identifier', 'firstname', 'lastname', 'date of birth',
            'gender',     'phone',     'status'
        )
        self.cand_table = DataTable.ParticipantsList( self.candidate_pane,
                                                      candidate_column_headers
                                                    )
        self.cand_table.pack(side=BOTTOM, expand=YES, fill=BOTH)
        # calendar table
        visit_column_headers = (
            'identifier', 'candidate', 'visitlabel', 'when', 'where', 'status'
        )
        self.visit_table = DataTable.VisitList( self.visit_pane,
                                                visit_column_headers
                                              )
        self.visit_table.pack(side=BOTTOM, expand=YES, fill=BOTH)

        """
        #create a filter section in each data_pane(not implemented yet)
        #TODO This whole section needs to be replaced by REAL CODE actively filtering the data
        self.filter_candidate = Labelframe(self.candidate_pane, text='Filters', width=220, height=50, borderwidth=10)
        self.filter_candidate.pack(side=TOP, expand=NO, fill=BOTH, pady=5)
        self.filter_candidate_label = Label(self.filter_candidate, text='Filter for Non-Active / Active / Excluded / Group...')
        self.filter_candidate_label.pack(side=TOP, expand=NO, fill=BOTH)
        self.filter_visit = Labelframe(self.visit_pane, text='Filters', width=220, height=50, borderwidth=10)
        self.filter_visit.pack(side=TOP, expand=NO, fill=BOTH, pady=5)
        self.filter_candidate_label = Label(self.filter_visit, text='Filters for Active / Tentative / Closed ...')
        self.filter_candidate_label.pack(side=TOP, expand=NO, fill=BOTH)
        """

    def add_candidate(self):
        DataWindow.DataWindow(self, "new")
        self.update_data(self.cand_table)


    def update_data(self, table):
        for i in table.datatable.get_children():
            table.datatable.delete(i)
        DataTable.ParticipantsList.load_data(table)
