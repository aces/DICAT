# import standard packages
from Tkinter import *
from ttk import *
# import internal packages
import ui.datawindow as DataWindow
import lib.datamanagement as DataManagement

class DataTable(Frame):
    """
    DataTable is a base class (which inherit from Frame) defining the functionalities of
    this Tkinter.ttk.treeview widget.
    Child clases are ParticipantsList(DataTable) and VisitList(DataTable)
    """

    def __init__(self, parent, colheaders, xmlfile):
        Frame.__init__(self)
        self.parent = parent
        self.init_datatable(parent, colheaders, xmlfile)

    """
    Initialize the datatable (which is a tk.treeview & add scroll bars)
    """
    def init_datatable(self, parent, colheaders, xmlfile):

        # initialize the treeview datatable
        self.datatable = Treeview( parent,             selectmode='browse',
                                   columns=colheaders, show="headings"
                                 )

        # add the column headers to the datatable
        for col in colheaders:
            self.datatable.heading(
                col,
                text=col.title(),
                command=lambda c=col: self.treeview_sortby(self.datatable, c, 0)
                                  )
            self.datatable.column( col,           width=100,
                                   stretch="Yes", anchor="center"
                                 )

        # add vertical and horizontal scroll
        self.verticalscroll = Scrollbar( parent, orient="vertical",
                                         command=self.datatable.yview
                                       )
        self.horizontalscroll = Scrollbar( parent, orient="horizontal",
                                           command=self.datatable.xview
                                         )
        self.datatable.configure( yscrollcommand=self.verticalscroll.set,
                                  xscroll=self.horizontalscroll.set
                                )
        self.verticalscroll.pack(side=RIGHT, expand=NO, fill=BOTH)
        self.horizontalscroll.pack(side=BOTTOM, expand=NO, fill=BOTH)

        # draw the datatable
        self.datatable.pack(side=LEFT, expand=YES, fill=BOTH)

        # bind with events
        self.datatable.bind('<Double-1>', lambda event: self.ondoubleclick(xmlfile, event))

        #self.datatable.bind('<Double-1>',         self.ondoubleclick(xmlfile))
        self.datatable.bind("<<TreeviewSelect>>", self.onrowclick   )
        self.datatable.bind('<Button-3>',         self.onrightclik  )

    def load_data(self):
        """Should be overriden in child class"""
        pass

    def update_data(self):
        for i in self.datatable.get_children():
            self.datatable.delete(i)
        self.load_data()

    def treeview_sortby(self, tree, column, descending):
        """
        Sort treeview contents when a column is clicked on.
        Taken from Dave's IDmapper
        From: https://code.google.com/p/python-ttk/source/browse/trunk/pyttk-samples/treeview_multicolumn.py?r=21
        """
        # grab values to sort
        data = [(tree.set(child, column), child) for child in tree.get_children('')]
        # reorder data
        data.sort(reverse=descending)
        for index, item in enumerate(data):
            tree.move(item[1], '', index)
            # switch the heading so that it will sort in the opposite direction
            tree.heading(column, command=lambda column=column: self.treeview_sortby(tree, column, int(not descending)))

    def ondoubleclick(self, xmlfile, event):
        """
        Double clicking on a treeview line opens a 'data window'
        and refresh the treeview data when the 'data window' is closed
        """

        # double clicking on blank space of the treeview when no valid line is selected generates a
        # IndexOutOfRange error which is taken care of by this try:except block
        try:
            itemID = self.datatable.selection()[0]
            item = self.datatable.item(itemID)['tags']
            parent = self.parent
            candidate_id = item[1]
            DataWindow.DataWindow(parent, xmlfile, candidate_id)
            self.update_data()
        except Exception as e:
            print "Datatable ondoubleclick ", str(e)  # TODO deal with exception or not!?!

    def onrightclik(self, event):
        """Not used yet"""
        print 'contextual menu for this item'
        pass

    def onrowclick(self, event):
        """Not used yet"""
        item_id = str(self.datatable.focus())
        item = self.datatable.item(item_id)['values']
        # print item_id, item  #TODO remove when done


class ParticipantsList(DataTable):
    """
    class ParticipantsList(DataTable) takes care of the data table holding the list of participants
    That list is comprised of all participants (even those that have not been called once.
    """

    def __init__(self, parent, colheaders, xmlfile):  # expected is dataset
        DataTable.__init__(self, parent, colheaders, xmlfile)
        self.colheaders = colheaders
        self.load_data(xmlfile)
        # TODO add these color settings in a 'settings and preferences section of the app'
        self.datatable.tag_configure('active', background='#F1F8FF')  # TODO replace active tag by status variable value

    def load_data(self, xmlfile):
        data = DataManagement.read_candidate_data(xmlfile)

        try:
            for key in data:

                if "CandidateStatus" not in data[key].keys():
                    status = ""
                else:
                    status = data[key]["CandidateStatus"]

                if "PhoneNumber" not in data[key].keys():
                    phone = ""
                else:
                    phone = data[key]["PhoneNumber"]
                self.datatable.insert( '', 'end',
                                       values=[ data[key]["Identifier"],
                                                data[key]["FirstName"],
                                                data[key]["LastName"],
                                                data[key]["Gender"],
                                                phone,
                                                status
                                              ],
                                       tags=(status, data[key]["Identifier"])
                                    )
        except Exception as e:
            print "datatable.ParticipantsList.load_data ", str(e)  # TODO proper exception handling
            pass


class VisitList(DataTable):
    """
    class VisitList(DataTable) takes care of the data table holding the list of all appointments
    even those that have not been confirmed yet.
    """

    def __init__(self, parent, colheaders, xmlfile):
        DataTable.__init__(self, parent, colheaders, xmlfile)
        self.colheaders = colheaders
        self.load_data(xmlfile)
        # TODO add these color settings in a 'settings and preferences section of the app'
        self.datatable.tag_configure('active', background='#F1F8FF')  # TODO change for non-language parameter
        self.datatable.tag_configure('tentative', background='#F0F0F0')  # TODO change for non-language parameter

    def load_data(self, xmlfile):
        data = dict(DataManagement.read_visitset_data(xmlfile))
        for cand_key, value in data.iteritems():
            if "VisitSet" in data[cand_key].keys():  # skip the search if visitset = None
                current_visitset = data[cand_key]["VisitSet"]  # set this candidate.visitset for the next step
                # gather information about the candidate
                candidate_id        = data[cand_key]["Identifier"]
                candidate_firstname = data[cand_key]["FirstName"]
                candidate_lastname  = data[cand_key]["LastName"]
                candidate_fullname  = str( candidate_firstname
                                           + ' '
                                           + candidate_lastname
                                         )
                for visit_key, value in current_visitset.iteritems():
                    if "VisitStatus" in current_visitset[visit_key].keys():
                        status = current_visitset[visit_key]["VisitStatus"]
                        visit_label = current_visitset[visit_key]["VisitLabel"]
                        if "VisitStartWhen" not in current_visitset[visit_key].keys():
                            when = ''  #TODO check what would be the next visit and set status to "to_schedule"
                            #when = current_visitset[visit_key].whenearliest
                        else:
                            when = current_visitset[visit_key]["VisitStartWhen"]
                        if "VisitWhere" not in current_visitset[visit_key].keys():
                            where = ''
                        else:
                            where = current_visitset[visit_key]["VisitWhere"]
                        try:
                            row_values = [ candidate_id, candidate_fullname,
                                           visit_label,  when,
                                           where,        status
                                         ]
                            row_tags = (status, candidate_id, visit_label)
                            self.datatable.insert('',
                                                  'end',
                                                  values = row_values,
                                                  tags   = row_tags
                                                 )
                        except Exception as e:
                            print "datatable.VisitList.load_data ", str(e)  # TODO add proper error handling
                            pass
