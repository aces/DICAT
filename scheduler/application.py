#!/usr/bin/env python

#import standard packages
from Tkinter import *
from ttk import *
#import internal packages
import ui.menubar as MenuBar
import ui.datatable as DataTable
import lib.multilanguage as MultiLanguage
import lib.datamanagement as DataManagement
import ui.projectpane as ProjectPane  #TODO create classe for project info pane

class UserInterface(Frame):
    def __init__(self, parent):
        Frame.__init__(self)
        self.parent = parent
        self.parent.title(MultiLanguage.app_title)
        self.pack(side=TOP, expand=YES, fill=BOTH, padx=10, pady=10)
        # TODO create classe for project info pane
        self.project_infopane = Labelframe(self, text=MultiLanguage.project_info_pane, width=250, height=350,
                                          borderwidth=10)  # TODO add dynamic resize
        self.project_infopane.pack(side=LEFT, expand=NO, fill=BOTH)
        # This area (datapane) is composed of one Panedwindow containing two Labelframe
        self.data_pane = Panedwindow(self, width=1000, height=500, orient=HORIZONTAL)  # TODO add dynamic resize
        self.data_pane.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.candidate_pane = Labelframe(self.data_pane, text=MultiLanguage.candidate_pane, width=100, height=450,
                                        borderwidth=10)  # TODO add dynamic resize
        self.visit_pane = Labelframe(self.data_pane, text=MultiLanguage.calendar_pane, width=100, height=350,
                                    borderwidth=10)  # TODO add dynamic resize
        self.data_pane.add(self.candidate_pane)
        self.data_pane.add(self.visit_pane)

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

        # get data from shelve files
        data = dict(DataManagement.read_candidate_data())  # TODO place data management elsewhere

        # create data tables (treeview)
        visit_column_headers = ('candidate', 'visitlabel', 'when', 'where', 'status')
        self.visit_table = DataTable.DataTable(self.visit_pane, data, visit_column_headers)
        self.visit_table.pack(side=BOTTOM, expand=YES, fill=BOTH)
        column_header = ('firstname', 'lastname', 'phone', 'status')
        self.data_table = DataTable.DataTable(self.candidate_pane, data, column_header)
        self.data_table.pack(side=BOTTOM, expand=YES, fill=BOTH)

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        menu = MenuBar.MenuBar(self)
        self.config(menu=menu)
        frame = UserInterface(self)

#Application main loop
if __name__ == "__main__":
    app=Application()
    app.mainloop()