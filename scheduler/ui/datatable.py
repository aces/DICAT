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

    def __init__(self, parent, colheaders):
        Frame.__init__(self)
        self.parent = parent
        colheaders = colheaders
        datatable = self.init_datatable(parent, colheaders)

    def init_datatable(self, parent, colheaders):
        """Initialize the datatable (which is a tk.treeview and add scroll bars)"""
        self.datatable = Treeview(parent, selectmode='browse', columns=colheaders, show="headings")
        for col in colheaders:
            self.datatable.heading(col, text=col.title(),
                                   command=lambda c=col: self.treeview_sortby(self.datatable, c, 0))
            self.datatable.column(col, width=100, stretch="Yes", anchor="center")
        # add vertical and horizontal scroll
        self.verticalscroll = Scrollbar(parent, orient="vertical", command=self.datatable.yview)
        self.horizontalscroll = Scrollbar(parent, orient="horizontal", command=self.datatable.xview)
        self.datatable.configure(yscrollcommand=self.verticalscroll.set, xscroll=self.horizontalscroll.set)
        self.verticalscroll.pack(side=RIGHT, expand=NO, fill=BOTH)
        self.horizontalscroll.pack(side=BOTTOM, expand=NO, fill=BOTH)
        self.datatable.pack(side=LEFT, expand=YES, fill=BOTH)
        # Binding with events
        self.datatable.bind('<Double-1>', self.ondoubleclick)
        self.datatable.bind("<<TreeviewSelect>>", self.onrowclick)
        self.datatable.bind('<Button-3>', self.onrightclik)

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

    def ondoubleclick(self, event):
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
            candidate_uuid = item[1]
            DataWindow.DataWindow(parent, candidate_uuid)
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

    def __init__(self, parent, colheaders):  # expected is dataset
        DataTable.__init__(self, parent, colheaders)
        self.colheaders = colheaders
        self.load_data()
        # TODO add these color settings in a 'settings and preferences section of the app'
        self.datatable.tag_configure('active', background='#F1F8FF')  # TODO replace active tag by status variable value

    def load_data(self):
        data = dict(DataManagement.read_candidate_data())
        try:
            for key in data:
                if data[key].status is None:
                    status = ''
                else:
                    status = data[key].status
                self.datatable.insert('', 'end',
                                      values=[data[key].firstname, data[key].lastname, data[key].phone,
                                              status], tags=(status, data[key].uid))
        except Exception as e:
            print "datatable.ParticipantsList.load_data ", str(e)  # TODO proper exception handling
            pass


class VisitList(DataTable):
    """
    class VisitList(DataTable) takes care of the data table holding the list of all appointments
    even those that have not been confirmed yet.
    """

    def __init__(self, parent, colheaders):
        DataTable.__init__(self, parent, colheaders)
        self.colheaders = colheaders
        self.load_data()
        # TODO add these color settings in a 'settings and preferences section of the app'
        self.datatable.tag_configure('active', background='#F1F8FF')  # TODO change for non-language parameter
        self.datatable.tag_configure('tentative', background='#F0F0F0')  # TODO change for non-language parameter

    def load_data(self):
        data = dict(DataManagement.read_candidate_data())
        for key, value in data.iteritems():
            if data[key].visitset is not None:  # skip the search if visitset = None
                current_visitset = data[key].visitset  # set this candidate.visitset for the next step
                # gather information about the candidate
                # this candidatekey is not printed on screen but saved with the new Scheduler object
                candidatekey = data[key].uid
                candidate_firstname = data[key].firstname
                candidate_lastname = data[key].lastname
                candidate_fullname = str(candidate_firstname + ' ' + candidate_lastname)
                for key, value in current_visitset.iteritems():
                    if current_visitset[key].status is not None:
                        status = current_visitset[key].status
                        visit_label = current_visitset[key].visitlabel
                        if current_visitset[key].when is None:
                            when = current_visitset[key].whenearliest
                        else:
                            when = current_visitset[key].when
                        if current_visitset[key].where is None:
                            where = ''
                        else:
                            where = current_visitset[key].where
                        try:
                            self.datatable.insert('', 'end',
                                                  values=[candidate_fullname, visit_label, when, where, status],
                                                  tags=(status, candidatekey, visit_label))
                        except Exception as e:
                            print "datatable.VisitList.load_data ", str(e)  # TODO add proper error handling
                            pass
