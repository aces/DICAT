# import standard packages
from Tkinter import *
from ttk import *

# import internal packages
import ui.datawindow as DataWindow
import lib.datamanagement as DataManagement

class DataTable(Frame):
    """
    DataTable is a base class (which inherits from Frame) defining the
    functionality of the Tkinter.ttk.treeview widget.
    Children classes are ParticipantsList(DataTable) and VisitList(DataTable)

    """


    def __init__(self, parent, colheaders):
        Frame.__init__(self)
        self.parent = parent
        self.init_datatable(parent, colheaders)


    def init_datatable(self, parent, colheaders):
        """
        Initialize datatable (which is a tk.treeview & add scroll bars)

        :param parent: frame in which the datatable should take place
         :type parent: frame
        :param colheaders: array with the list of column header strings
         :type colheaders: list

        """

        # Initialize the Treeview datatable
        self.datatable = Treeview(
            parent, selectmode='browse', columns=colheaders, show="headings"
        )

        # Add column headers to datatable
        for col in colheaders:
            self.datatable.heading(
                col,
                text=col.title(),
                command=lambda c=col: self.treeview_sortby(
                    self.datatable, c, 0
                )
            )
            self.datatable.column(
                col, width=100, stretch="Yes", anchor="center"
            )

        # Add vertical and horizontal scroll bars
        self.verticalscroll = Scrollbar(
            parent, orient="vertical", command=self.datatable.yview
        )
        self.horizontalscroll = Scrollbar(
            parent, orient="horizontal", command=self.datatable.xview
        )
        self.datatable.configure(
            yscrollcommand=self.verticalscroll.set,
            xscroll=self.horizontalscroll.set
        )
        self.verticalscroll.pack(   side=RIGHT,  expand=NO, fill=BOTH )
        self.horizontalscroll.pack( side=BOTTOM, expand=NO, fill=BOTH )

        # Draw the datatable
        self.datatable.pack( side=LEFT, expand=YES, fill=BOTH )

        # Bind with events
        self.datatable.bind('<Double-1>',         self.ondoubleclick)
        self.datatable.bind("<<TreeviewSelect>>", self.onrowclick   )
        self.datatable.bind('<Button-3>',         self.onrightclik  )


    def load_data(self):
        """
        Should be overriden in child's class

        """
        pass


    def update_data(self):
        """
        Delete everything in datatable and reload its content with the updated
        data coming from the XML file.

        """

        for i in self.datatable.get_children():
            self.datatable.delete(i) # delete all data from the datatable
        self.load_data() # reload all data with updated values


    def treeview_sortby(self, tree, column, descending):
        """
        Sort treeview contents when a column is clicked on.

        :param tree: treview table
         :type tree:
        :param column: column to sort by
         :type column:
        :param descending: descending sorting
         :type descending:

        """

        # grab values to sort
        data = \
           [(tree.set(child, column), child) for child in tree.get_children('')]

        # reorder data
        data.sort(reverse=descending)
        for index, item in enumerate(data):
            tree.move(item[1], '', index)

            # switch the heading so that it will sort in the opposite direction
            tree.heading(
                column,
                command=lambda column=column: self.treeview_sortby(
                    tree, column, int(not descending)
                )
            )


    def ondoubleclick(self, event):
        """
        Double clicking on a treeview line opens a 'data window'.
        Treeview data will be reloaded once the 'data window' has been closed.

        :param event:
         :type event:

        """

        # Double click on a blank line of the Treeview datatable generates an
        # IndexOutOfRange error which is taken care of by this try:except block
        try:
            itemID = self.datatable.selection()[0]
            item   = self.datatable.item(itemID)['tags']
            parent = self.parent
            candidate_id = item[1]
            DataWindow.DataWindow(parent, candidate_id)
            self.update_data()

        except Exception as e:
            # TODO: deal with exceptions
            print "Datatable ondoubleclick ", str(e)


    def onrightclik(self, event): #TODO: to implement this or not?
        """
        Not used yet

        :param event:
         :type event:

        """

        print 'contextual menu for this item'
        pass


    def onrowclick(self, event):  #TODO: to implement this or not?
        """
        Not used yet

        :param event:
         :type event:

        """

        item_id = str(self.datatable.focus())
        item = self.datatable.item(item_id)['values']




class ParticipantsList(DataTable):
    """
    Class ParticipantsList(DataTable) takes care of the data table holding the
    list of participants. That list contains all participants (even those that
    have never been called).

    """

    def __init__(self, parent, colheaders):  # expected is dataset
        """
        __init__ function of ParticipantsList class

        :param parent: frame in which to insert the candidate datatable
         :type parent: frame
        :param colheaders: array of column headers to use in the datatable
         :type colheaders: list

        """

        DataTable.__init__(self, parent, colheaders)

        self.colheaders = colheaders  # initialize the column headers
        self.load_data()              # load the data in the datatable

        # TODO add color settings in a 'settings & preferences' section
        # TODO replace 'active' tag by status variable value
        self.datatable.tag_configure('active', background='#F1F8FF')


    def load_data(self):
        """
        Load candidates information into the candidate datatable.

        """
        
        # Read candidates information into a cand_data dictionary
        cand_data = DataManagement.read_candidate_data()

        try:
            # Loop through all candidates
            for key in cand_data:

                # Deal with occurences where CandidateStatus is not set
                if "CandidateStatus" not in cand_data[key].keys():
                    status = ""
                else:
                    status = cand_data[key]["CandidateStatus"]

                # Deal with occurences where PhoneNumber is not set
                if "PhoneNumber" not in cand_data[key].keys():
                    phone = ""
                else:
                    phone = cand_data[key]["PhoneNumber"]
                
                # Insert a given candidate into the datatable
                self.datatable.insert(
                    '', 
                    'end', 
                    values=[ 
                        cand_data[key]["Identifier"],
                        cand_data[key]["FirstName"],
                        cand_data[key]["LastName"],
                        cand_data[key]["DateOfBirth"],
                        cand_data[key]["Gender"],
                        phone,
                        status
                    ],
                    tags=(status, cand_data[key]["Identifier"])
                )

        except Exception as e:  # TODO proper exception handling
            print "datatable.ParticipantsList.load_data ", str(e)
            pass




class VisitList(DataTable):
    """
    This class takes care of the data table holding the list of all
    appointments, even those that have not been confirmed yet.

    """

    def __init__(self, parent, colheaders):
        """
        __init__ function of ParticipantsList class

        :param parent: frame in which to insert the visit list datatable
         :type parent: frame
        :param colheaders: array of column headers to use in the datatable
         :type colheaders: list

        """

        DataTable.__init__(self, parent, colheaders)

        self.colheaders = colheaders  # initialize the column headers
        self.load_data()              # load the data in the datatable

        # TODO add color settings in a 'settings and preferences' section
        # TODO change 'active' & 'tentative' for non-language parameter
        self.datatable.tag_configure('active', background='#F1F8FF')
        self.datatable.tag_configure('tentative', background='#F0F0F0')


    def load_data(self):
        """
        Load the visit list into the datatable.

        """

        # Read visit list and visit information into a visit_data dictionary
        visit_data = DataManagement.read_visitset_data()

        try:
            # Loop through candidates
            for cand_key, value in visit_data.iteritems():

                # Skip the search if visitset == None for that candidate
                if "VisitSet" in visit_data[cand_key].keys():

                    # set this candidate.visitset for the next step
                    current_visitset = visit_data[cand_key]["VisitSet"]

                    # gather information about the candidate
                    candidate_id        = visit_data[cand_key]["Identifier"]
                    candidate_firstname = visit_data[cand_key]["FirstName"]
                    candidate_lastname  = visit_data[cand_key]["LastName"]
                    candidate_fullname  = str(
                        candidate_firstname + ' ' + candidate_lastname
                    )

                    # Loop through all visits for that candidate
                    for visit_key, value in current_visitset.iteritems():

                        if "VisitStatus" in current_visitset[visit_key].keys():
                            # Set visit status and label
                            status = current_visitset[visit_key]["VisitStatus"]
                            visit_label = current_visitset[visit_key]["VisitLabel"]

                            # Check at what time the visit has been scheduled
                            field = 'VisitStartWhen'
                            if field not in current_visitset[visit_key].keys():
                                when = ''
                                #TODO check what would be next visit
                                #TODO & set its status to "to_schedule"
                                #when = current_visitset[visit_key].whenearliest

                            else:
                                when_key = 'VisitStartWhen'
                                when = current_visitset[visit_key][when_key]

                            # Check if the location of the visit has been set
                            field = 'VisitWhere'
                            if field not in current_visitset[visit_key].keys():
                                where = ''

                            else:
                                where = current_visitset[visit_key]["VisitWhere"]
                            # Check that all values could be found
                            row_values = [
                                candidate_id, candidate_fullname, visit_label,
                                when,         where,              status
                            ]
                            row_tags = (status, candidate_id, visit_label)
                            self.datatable.insert(
                                '', 'end', values = row_values, tags = row_tags
                            )

        except Exception as err:
            #TODO deal with exception
            #TODO add proper error handling
            print "Could not load visits"
            pass
