#!/usr/bin/env python

#import standard packages
from Tkinter import *
from ttk import *
#import internal packages
import ui.menubar as MenuBar
import ui.datatable as DataTable
import lib.multilanguage as MultiLanguage


class UserInterface(Frame):

    def __init__(self, parent):
        Frame.__init__(self)
        self.parent = parent
        #self.parent.title(MultiLanguage.app_title)
        self.initialize()

    def initialize(self):
        self.frame = Frame(self.parent)
        self.frame.pack(side=TOP, expand=YES, fill=BOTH, padx=10, pady=10)
        # TODO create classe for project info pane
        self.frame.project_infopane = Labelframe(self, text=MultiLanguage.project_info_pane, width=250, height=350,
                                          borderwidth=10)  # TODO add dynamic resize
        self.frame.project_infopane.pack(side=LEFT, expand=NO, fill=BOTH)
        # This area (datapane) is composed of one Panedwindow containing two Labelframe
        self.frame.data_pane = Panedwindow(self, width=1000, height=500, orient=HORIZONTAL)  # TODO add dynamic resize
        self.frame.data_pane.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.frame.candidate_pane = Labelframe(self.frame.data_pane, text=MultiLanguage.candidate_pane, width=100, height=450,
                                        borderwidth=10)  # TODO add dynamic resize
        self.frame.visit_pane = Labelframe(self.frame.data_pane, text=MultiLanguage.calendar_pane, width=100, height=350,
                                    borderwidth=10)  # TODO add dynamic resize
        self.frame.data_pane.add(self.frame.candidate_pane)
        self.frame.data_pane.add(self.frame.visit_pane)

        # create data tables (treeview)
        visit_column_headers = ('candidate', 'visitlabel', 'when', 'where', 'status')
        self.frame.visit_table = DataTable.VisitList(self.frame.visit_pane, visit_column_headers)
        self.frame.visit_table.pack(side=BOTTOM, expand=YES, fill=BOTH)
        column_header = ('firstname', 'lastname', 'phone', 'status')
        self.frame.data_table = DataTable.ParticipantsList(self.frame.candidate_pane, column_header)
        self.frame.data_table.pack(side=BOTTOM, expand=YES, fill=BOTH)

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


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        menu = MenuBar.MenuBar(self)
        self.config(menu=menu)
        frame = UserInterface(self)

"""
#Application main loop
if __name__ == "__main__":
    app=Application()
    app.mainloop()
"""
#Application main loop
app=Application()
app.mainloop()