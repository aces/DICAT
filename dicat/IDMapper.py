#!/usr/bin/python

from Tkinter import *
import ttk
import re

import lib.datamanagement as DataManagement
from lib.candidate import Candidate
import lib.multilanguage as MultiLanguage


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
        Initialize the ID Mapper GUI by calling self.init_ui().

        """

        # Initialize GUI
        self.init_ui()


    def init_ui(self):
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
            command=self.add_identifier_event
        )
        self.buttonClear  = Button(
            self.frame,
            width=12,
            text=u'Clear fields and filters',
            command=self.clear_event
        )
        self.buttonSearch = Button(
            self.frame,
            width=12,
            text=u'Search candidate',
            command=self.search_event
        )
        self.buttonEdit   = Button(
            self.frame,
            width=12,
            text=u'Edit candidate',
            command=self.edit_event
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

        self.datatable.bind("<<TreeviewSelect>>", self.on_row_click_event)
      
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


    def load_xml(self):
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


    def add_identifier_event(self):
        """
        Event handler for the 'Add new candidate' button. Will call
        check_and_save_data on what has been entered in the Entry boxes.

        """
        
        firstname = self.candidateFirstName.get()
        lastname  = self.candidateLastName.get()
        candid    = self.candidateid.get()
        dob       = self.candidateDoB.get()
        self.check_and_save_data(candid, firstname, lastname, dob, 'save')


    def on_row_click_event(self, event):
        """
        Update the text boxes' data on row click.

        """

        item_id = str(self.datatable.focus())
        item = self.datatable.item(item_id)['values']
        
        self.textCandId.set(item[0])
        self.textCandFirstName.set(item[1])
        self.textCandLastName.set(item[2])
        self.textCandDoB.set(item[3])


    def clear_event(self):
        """
        Event handler for the clear_event button. Will clear_event all the
        Entry boxes.

        """

        self.textCandId.set("")
        self.textCandFirstName.set("")
        self.textCandLastName.set("")
        self.textCandDoB.set("")
        self.candidateid.focus_set()

        self.load_xml() # Reload the entire dataset.


    def search_event(self):
        """
        Event handler for the search_event button. Will call find_candidate
        function to find the proper candidate matching what has been filled in
        the Entry boxes.

        """

        # Grep the data from the Entry fields
        data_captured = {}
        if self.textCandId.get():
            data_captured['Identifier']  = self.textCandId.get()
        if self.textCandFirstName.get():
            data_captured['FirstName']   = self.textCandFirstName.get()
        if self.textCandLastName.get():
            data_captured['LastName']    = self.textCandLastName.get()
        if self.textCandDoB.get():
            data_captured['DateOfBirth'] = self.textCandDoB.get()

        # If no data entered, write a message saying at least one field should
        # be entered and return
        if not data_captured:
            message = MultiLanguage.dialog_no_data_entered
            self.ErrorMessage.set(message)
            return

        # Use the function find_candidate to find all matching candidates and
        # return them in the filtered data dictionary
        filtered_data = self.find_candidate(data_captured)

        # Display only the filtered data using DisplayCandidates(filtered_data)
        self.display_filtered_data(filtered_data)


    def find_candidate(self, data_captured):
        """
        Find a candidate based on one of the fields entered in the Entry boxes.

        :param data_captured: dictionary of the data captured in the Entry boxes
         :type data_captured: dict

        :return filtered_data: dictionary of the matching candidates
         :rtype filtered_data: dict

        """

        global data

        # Loop through the candidate tree and return the candid, name and dob
        # that matches a given value
        # Create a filtered_data dictionary that will store all matching
        # candidates
        filtered_data = {}
        # Create an 'add' boolean on whether should add a candidate to the
        # filtered list and set it to False
        add = False
        for cand_key in data:
            # Grep the candidate information from data
            candid    = data[cand_key]["Identifier"]
            firstname = data[cand_key]["FirstName"]
            lastname  = data[cand_key]["LastName"]
            dob       = data[cand_key]["DateOfBirth"]
            if 'DateOfBirth' in data_captured \
                    and re.match(data_captured['DateOfBirth'], dob):
                add = True # set the 'add' boolean to true to add candidate
            if 'FirstName' in data_captured \
                    and re.match(data_captured['FirstName'], firstname):
                add = True # set the 'add' boolean to true to add candidate
            if 'LastName' in data_captured \
                    and re.match(data_captured['LastName'], lastname):
                add = True # set the 'add' boolean to true to add candidate
            if 'Identifier' in data_captured \
                    and re.match(data_captured['Identifier'], candid):
                add = True # set the 'add' boolean to true to add candidate

            # If add is set to True, add the candidate to the filtered list.
            if add:
                filtered_data[cand_key] = data[cand_key]
                add = False # reset the 'add' boolean to false for next cand_key

        return filtered_data


    def display_filtered_data(self, filtered_data):
        """
        Displays only the filtered data matching the search_event.

        :param filtered_data: dictionary of the matching candidates
         :type filtered_data: dict

        """

        # Empty the datatable and data dictionary before loading filtered data
        self.datatable.delete(*self.datatable.get_children())
        self.IDMap = {}

        # Loop through the data and display them in the datatable
        for key in filtered_data:
                identifier = filtered_data[key]["Identifier"]
                firstname  = filtered_data[key]["FirstName"]
                lastname   = filtered_data[key]["LastName"]
                dob = filtered_data[key]["DateOfBirth"]
                self.check_and_save_data(
                    identifier, firstname, lastname, dob, False
                )


    def edit_event(self):
        """
        Edit event of the Edit button. Will call check_and_save_date with
        data entered in the Entry boxes and action='edit_event'.

        """

        self.check_and_save_data(
            self.textCandId.get(),
            self.textCandFirstName.get(),
            self.textCandLastName.get(),
            self.textCandDoB.get(),
            'edit'
        )


    def check_and_save_data(self, id, firstname, lastname, dob, action=False):
        """
        Grep the candidate data and check them before saving and updating the
        XML file and the datatale.

        :param id: identifier of the candidate
         :type id: str
        :param firstname: firstname of the candidate
         :type firstname: str
        :param lastname: lastname of the candidate
         :type lastname: str
        :param dob: date of birth of the candidate
         :type dob: str
        :param action: either 'save' new candidate or 'edit' a candidate
         :type action: bool/str

        :return:

        """

        # Check all required data are available
        cand_data = {}
        cand_data["Identifier"]  = id
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
            message = candidate.check_candidate_data('IDmapper', id)

        # If message contains an error message, display it and return
        if message:
            self.ErrorMessage.set(message)
            return

        # Save the candidate data in the XML
        DataManagement.save_candidate_data(cand_data)

        # Update the IDMap dictionary
        mapList = [id, firstname, lastname, dob]
        self.IDMap[id] = mapList

        # Update datatable
        if action == 'edit':
            item = self.datatable.selection()
            updatedList = (id, firstname, lastname, dob)
            self.datatable.item(item, values=updatedList)
        else:
            insertedList = [(id, firstname, lastname, dob)]
            for item in insertedList:
                self.datatable.insert('', 'end', values=item)




def main():
       
    root = Tk()
    app = IDMapper_frame_gui(root)
    root.mainloop()
 

if __name__ == "__main__":
    main()
