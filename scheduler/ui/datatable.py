#import standard packages
from Tkinter import *
from ttk import *
#import internal packages
import ui.datawindow as DataWindow

class DataTable(Frame):
    def __init__(self, parent, dataset, colheaders):  # expected is dataset
        Frame.__init__(self)
        self.parent = parent
        colheaders = colheaders
        dataset = dataset
        datatable = self.init_datatable(parent, colheaders)
        self.load_data(datatable, dataset, colheaders)

    def init_datatable(self, parent, colheaders):
        self.datatable = Treeview(parent, selectmode='browse', columns=colheaders, show="headings")
        for col in colheaders:
            self.datatable.heading(col, text=col.title(),
                                   command=lambda c=col: self.treeview_sortby(self.datatable, c, 0))
            self.datatable.column(col, width=100, stretch="Yes", anchor="center")
        #add vertical and horizontal scroll
        self.verticalscroll = Scrollbar(parent, orient="vertical", command=self.datatable.yview)
        self.horizontalscroll = Scrollbar(parent, orient="horizontal", command=self.datatable.xview)
        self.datatable.configure(yscrollcommand=self.verticalscroll.set, xscroll=self.horizontalscroll.set)
        self.verticalscroll.pack(side=RIGHT, expand=NO, fill=BOTH)
        self.horizontalscroll.pack(side=BOTTOM, expand=NO, fill=BOTH)
        self.datatable.pack(side=LEFT, expand=YES, fill=BOTH)

    def treeview_sortby(self, tree, column, descending):
        """Taken from Dave's IDmapper"""
        """Sort tree contents when a column is clicked on."""
        """From: https://code.google.com/p/python-ttk/source/browse/trunk/pyttk-samples/treeview_multicolumn.py?r=21"""
        # grab values to sort
        data = [(tree.set(child, column), child) for child in tree.get_children('')]
        # reorder data
        data.sort(reverse=descending)
        for index, item in enumerate(data):
            tree.move(item[1], '', index)
            # switch the heading so that it will sort in the opposite direction
            tree.heading(column, command=lambda column=column: self.treeview_sortby(tree, column, int(not descending)))

    # TODO move to dataManagement
    # Need to re-write this section
    def load_data(self, datatable, dataset, colheaders):
        if 'firstname' in colheaders:
            # This method will add cantidates information to cantidatetable
            try:
                for key in dataset:
                    if dataset[key].status is None:
                        status = ''
                    else:
                        status = dataset[key].status
                    self.datatable.insert('', 'end',
                                          values=[dataset[key].firstname, dataset[key].lastname, dataset[key].phone,
                                                  status], tags=(status, dataset[key].uid))
            except Exception as e:
                print str(e)
                # utilities.errorlog(message)
                pass  # TODO add some error handling

            # TODO add these color settings in a 'settings and preferences section of the app'
            self.datatable.tag_configure('active', background='#F1F8FF')
            # Behavior of datatable on single and double click
            self.datatable.bind('<Double-1>', self.ondoubleclick)
            self.datatable.bind("<<TreeviewSelect>>", self.onrowclick)
            self.datatable.bind('<Button-3>', self.onrightclik)

        elif 'candidate' in colheaders:
            for key, value in dataset.iteritems():
                if dataset[key].visitset is not None:  # skip the search if visitset = None
                    currentvisitset = dataset[key].visitset  # set this candidate.visitset for the next step
                    # gather information about the candidate
                    # this candidatekey is not printed on screen but saved with the new Scheduler object
                    # (after all it is the candidate unique id^^)
                    candidatekey = dataset[key].uid

                    candidatefirstname = dataset[key].firstname
                    candidatelastname = dataset[key].lastname
                    candidatefullname = str(candidatefirstname + ' ' + candidatelastname)
                    for key, value in currentvisitset.iteritems():
                        if currentvisitset[key].status is not None:
                            visitlabel = currentvisitset[key].visitlabel
                            if currentvisitset[key].when is None:
                                when = currentvisitset[key].whenearliest
                            else:
                                when = currentvisitset[key].when
                            if currentvisitset[key].where is None:
                                where = ''
                            else:
                                where = currentvisitset[key].where
                            if currentvisitset[key].status is None:
                                status = ''
                            else:
                                status = currentvisitset[key].status
                            # TODO ? create a new scheduler object with these informations
                            # This method will add planned visits information to the visit datatable
                            try:
                                self.datatable.insert('', 'end',
                                                      values=[candidatefullname, visitlabel, when, where, status],
                                                      tags=(status, candidatekey, visitlabel))
                            except Exception as e:
                                print "Exception AddIdentifierAction(self, dataset, save=True): " + str(
                                    e)  # TODO dd some error handling
                                pass

            # TODO add these color settings in a 'settings and preferences section of the app'
            self.datatable.tag_configure('active',background='#F1F8FF')
            self.datatable.tag_configure('tentative',background='#F0F0F0')
            # Behavior of datatable on single and double click
            self.datatable.bind('<Double-1>', self.ondoubleclick)
            self.datatable.bind("<<TreeviewSelect>>", self.onrowclick)
            self.datatable.bind('<Button-3>', self.onrightclik)

    def ondoubleclick(self, event):
        # double clicking on blank space of the treeview when no valide line is selected generates an IndexOutOfRange
        # error which is taken care of by this try:except block
        try:
            itemID = self.datatable.selection()[0]
            item =self.datatable.item(itemID)['tags']
            parent = self.parent
            candidate_uuid = item[1]
            DataWindow.DataWindow(parent, candidate_uuid)
        except Exception as e:
            print str(e) #TODO deal with exception or not!?!

    def onrightclik(self, event):
        print 'contextual menu for this item'
        pass

    def onrowclick(self,event):
        item_id = str(self.datatable.focus())
        item = self.datatable.item(item_id)['values']
        print item_id, item