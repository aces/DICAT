#!/usr/bin/python

from Tkinter import *
import ttk

import lib.datamanagement as DataManagement
from lib.candidate import Candidate


def sortby(tree, col, descending):
    """Sort tree contents when a column is clicked on."""
    """From: https://code.google.com/p/python-ttk/source/browse/trunk/pyttk-samples/treeview_multicolumn.py?r=21"""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]

    # reorder data
    data.sort(reverse=descending)
    for indx, item in enumerate(data):
        tree.move(item[1], '', indx)

    # switch the heading so that it will sort in the opposite direction
    tree.heading(col,
        command=lambda col=col: sortby(tree, col, int(not descending)))

  
class IDMapper_frame_gui(Frame):
    
    def __init__(self, parent):
        """
        Initialize the ID Mapper frame.

        """

        self.parent = parent

        # Set up the dictionary map
        self.IDMap = {}

        # Initialize the frame
        self.initialize()


    def initialize(self):
        """
        Initialize the ID Mapper GUI by calling self.InitUI().

        """

        # Initialize GUI
        self.InitUI()


    def InitUI(self):
        """
        Draws the ID Mapper GUI.

        """
        
        self.frame = Frame(self.parent)
        self.frame.pack(expand=1, fill='both')

        for i in range(0, 3):
            self.frame.columnconfigure(i, weight=6)
        self.frame.columnconfigure(3, weight=1)
        
        for i in range(3, 4):
            self.frame.rowconfigure(i, weight=1)

        self.labelID        = Label(self.frame, text=u'Identifier')
        self.labelFirstName = Label(self.frame, text=u'First Name')
        self.labelLastName  = Label(self.frame, text=u'Last Name')
        self.labelDoB       = Label(
            self.frame, text=u'Date of Birth (YYYY-MM-DD)'
        )

        self.buttonAdd    = Button(
            self.frame,
            width=12,
            text=u'Add candidate',
            command=self.AddIdentifierEvent
        )
        self.buttonClear  = Button(
            self.frame, width=12, text=u'Clear fields', command=self.clear
        )
        self.buttonSearch = Button(
            self.frame, width=12, text=u'Search candidate', command=self.search
        )
        self.buttonEdit   = Button(
            self.frame, width=12, text=u'Edit candidate', command=self.edit
        )

        self.textCandId  = StringVar()
        self.candidateid = Entry(
            self.frame, textvariable=self.textCandId, width=20
        )
        self.candidateid.focus_set()

        self.textCandFirstName  = StringVar()
        self.candidateFirstName = Entry(
            self.frame, textvariable=self.textCandFirstName, width=20
        )

        self.textCandLastName  = StringVar()
        self.candidateLastName = Entry(
            self.frame, textvariable=self.textCandLastName, width=20
        )

        self.textCandDoB  = StringVar()
        self.candidateDoB = Entry(
            self.frame, textvariable=self.textCandDoB, width=20
        )

        self.tableColumns = (
            "Identifier", "First Name", "Last Name", "Date of Birth"
        )
        self.datatable    = ttk.Treeview(
            self.frame,
            selectmode='browse',
            columns=self.tableColumns,
            show="headings"
        )
        for col in self.tableColumns:
            self.datatable.heading(
                col,
                text=col.title(),
                command=lambda c=col: sortby(self.datatable, c, 0)
            )

        self.datatable.bind("<<TreeviewSelect>>", self.OnRowClick)
      
        self.ErrorMessage = StringVar()
        self.error = Label(self.frame, textvariable=self.ErrorMessage, fg='red')

        self.labelID.grid(       row=0, column=0, padx=(0,4), sticky=E+W)
        self.labelFirstName.grid(row=0, column=1, padx=(4,4), sticky=E+W)
        self.labelLastName.grid( row=0, column=2, padx=(4,4), sticky=E+W)
        self.labelDoB.grid(      row=0, column=3, padx=(4,4), sticky=E+W)

        self.candidateid.grid(
            row=1, column=0, padx=(0,4), pady=(0,10), sticky=E+W
        )
        self.candidateFirstName.grid(
            row=1, column=1, padx=(4,4), pady=(0,10), sticky=E+W
        )
        self.candidateLastName.grid(
            row=1, column=2, padx=(4,4), pady=(0,10), sticky=E+W
        )
        self.candidateDoB.grid(
            row=1, column=3, padx=(4,4), pady=(0,10), sticky=E+W
        )
 
        self.buttonClear.grid( row=2, column=0, padx=(4,0), sticky=E+W)
        self.buttonSearch.grid(row=2, column=1, padx=(4,0), sticky=E+W)
        self.buttonEdit.grid(  row=2, column=2, padx=(4,0), sticky=E+W)
        self.buttonAdd.grid(   row=2, column=3, padx=(4,0), sticky=E+W)

        self.datatable.grid(
            row=3, column=0, columnspan=4, pady=10, sticky='nsew'
        )
        self.error.grid(row=4, column=0, columnspan=4)


    def LoadXML(self):
        """
        Parses the XML file and loads the data into the IDMapper.
        Calls check_and_save_data with option action=False as we don't want to
        save the candidates to be added to the datatable back in the XML.

        """

        global data

        # empty the datatable and data dictionary before loading new file
        self.datatable.delete(*self.datatable.get_children())
        self.IDMap = {}

        try:
            data = DataManagement.read_candidate_data()
            for key in data:
                identifier = data[key]["Identifier"]
                firstname  = data[key]["FirstName"]
                lastname   = data[key]["LastName"]
                dob = data[key]["DateOfBirth"]
                self.check_and_save_data(
                    identifier, firstname, lastname, dob, False
                )
        except Exception as e:
            #TODO add error login (in case a candidate data file does not exist)
            print str(e)


    def AddIdentifierEvent(self):
        """
        Event handler for the 'Add new candidate' button. Will call
        check_and_save_data on what has been entered in the Entry boxes.

        """
        
        firstname = self.candidateFirstName.get()
        lastname  = self.candidateLastName.get()
        candid    = self.candidateid.get()
        dob       = self.candidateDoB.get()
        self.check_and_save_data(candid, firstname, lastname, dob, 'save')


    def OnRowClick(self, event):
        """
        Update the text boxes' data on row click.

        """

        item_id = str(self.datatable.focus())
        item = self.datatable.item(item_id)['values']
        
        self.textCandId.set(item[0])
        self.textCandFirstName.set(item[1])
        self.textCandLastName.set(item[2])
        self.textCandDoB.set(item[3])


    def clear(self):
        """
        Event handler for the clear button. Will clear all the Entry boxes.

        """

        self.textCandId.set("")
        self.textCandFirstName.set("")
        self.textCandLastName.set("")
        self.textCandDoB.set("")
        self.candidateid.focus_set()


    def search(self):
        """
        Event handler for the search button. Will call FindCandidate function
        to find the proper candidate matching what has been filled in the Entry
        boxes.

        """

        #  Find a candidate based on its ID if it is set in text box
        if self.textCandId.get():
            (candid, firstname, lastname, dob) = self.FindCandidate(
                "candid", self.textCandId.get()
            )
        # or based on its name if it is set in text box
        elif self.textCandFirstName.get():
            (candid, firstname, lastname, dob) = self.FindCandidate(
                "firstname", self.textCandFirstName.get()
            )
        elif self.textCandLastName.get():
            (candid, firstname, lastname, dob) = self.FindCandidate(
                "lastname", self.textCandLastName.get()
            )

        # print the values in the text box
        self.textCandId.set(candid)
        self.textCandFirstName.set(firstname)
        self.textCandLastName.set(lastname)
        self.textCandDoB.set(dob)


    def FindCandidate(self, key, value):
        """
        Find a candidate based on one of the fields entered in the Entry boxes.

        :param key: the name of the Entry type (a.k.a. 'candid', 'firstname'...)
         :type key: str
        :param value: the value stored in the Entry box (a.k.a. 'MTL0001' ... )
         :type value: str

        :return candid, firstname, lastname, dob: found candidate
         :rtype candid, firstname, lastname, dob: str

        """

        global data

        # Loop through the candidate tree and return the candid, name and dob
        # that matches a given value
        for cand_key in data:
            candid    = data[cand_key]["Identifier"]
            firstname = data[cand_key]["FirstName"]
            lastname  = data[cand_key]["LastName"]
            dob       = data[cand_key]["DateOfBirth"]
            if (key == "candid" and value == candid):
                return (candid, firstname, lastname, dob)
            elif (key == "firstname" and value == firstname):
                return (candid, firstname, lastname, dob)
            elif (key == "lastname" and value == lastname):
                return (candid, firstname, lastname, dob)
            elif (key == "dob" and value == dob):
                return (candid, firstname, lastname, dob)
            else:
                continue
        # if candidate was not found, return empty strings
        return ("", "", "")


    def edit(self):
        """
        Edit event of the Edit button. Will call check_and_save_date with
        data entered in the Entry boxes and action='edit'.

        """

        self.check_and_save_data(
            self.textCandId.get(),
            self.textCandFirstName.get(),
            self.textCandLastName.get(),
            self.textCandDoB.get(),
            'edit'
        )


    def check_and_save_data(self, candid, firstname, lastname, dob, action=False):
        """
        Grep the candidate data and check them before saving and updating the
        XML file and the datatale.

        :param candid: identifier of the candidate
         :type candid: str
        :param firstname: firstname of the candidate
         :type firstname: str
        :param lastname: lastname of the candidate
         :type lastname: str
        :param dob: date of birth of the candidate
         :type dob: str
        :param action: whether to 'save' a new candidate or 'edit' a candidate
         :type action: bool/str

        :return:

        """

        # Check all required data are available
        cand_data = {}
        cand_data["Identifier"]  = candid
        cand_data["FirstName"]   = firstname
        cand_data["LastName"]    = lastname
        cand_data["DateOfBirth"] = dob
        candidate = Candidate(cand_data)

        # Initialize message to False. Will be replaced by the appropriate error
        # message if checks failed.
        message = False
        if action == 'save':
            message = candidate.check_candidate_data('IDmapper', False)
        elif action == 'edit':
            message = candidate.check_candidate_data('IDmapper', candid)

        # If message contains an error message, display it and return
        if message:
            self.ErrorMessage.set(message)
            return

        # Save the candidate data in the XML
        DataManagement.save_candidate_data(cand_data)

        # Update the IDMap dictionary
        mapList = [candid, firstname, lastname, dob]
        self.IDMap[candid] = mapList

        # Update datatable
        if action == 'edit':
            item = self.datatable.selection()
            updatedList = (candid, firstname, lastname, dob)
            self.datatable.item(item, values=updatedList)
        else:
            insertedList = [(candid, firstname, lastname, dob)]
            for item in insertedList:
                self.datatable.insert('', 'end', values=item)




def main():
       
    root = Tk()
    app = IDMapper_frame_gui(root)
    root.mainloop()
 

if __name__ == "__main__":
    main()
