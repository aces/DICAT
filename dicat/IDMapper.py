#!/usr/bin/python

import Tkinter, Tkconstants, tkFileDialog, tkMessageBox, re, datetime
from Tkinter import *

import lib.datamanagement as DataManagement
import lib.config as Config


import ttk

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
        """Initialize the application"""
        self.parent = parent

        # Set up the dictionary map
        self.IDMap = {}

        # Initialize the frame
        self.initialize()


    def initialize(self):

        # initialize Frame
        self.frame = Frame(self.parent)
        self.frame.pack(expand=1, fill='both')
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=6)


        # select an existing candidate.xml file
        # Initialize default text that will be in self.entry
        self.entryVariable = Tkinter.StringVar()
        self.entryVariable.set("Open an XML file with candidate's key")

        # Create an entry with a default text that will be replaced by the path
        # to the XML file once directory selected
        self.entry = Entry(self.frame,
                           width=40,
                           textvariable=self.entryVariable
                          )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

        # Create an open button to use to select an XML file with candidate's
        # key info
        self.buttonOpen = Button(self.frame,
                                 text=u"Open an existing file",
                                 command=self.openfilename
                                )

        self.buttonCreate = Button(self.frame,
                                   text=u"Create a new file",
                                   command=self.createfilename
                                  )

        self.buttonCreate.grid(row=0,
                               column=0,
                               padx=(0, 15),
                               pady=10,
                               sticky=E + W
                              )
        self.buttonOpen.grid(row=0,
                             column=1,
                             padx=(0, 15),
                             pady=10,
                             sticky=E + W
                            )
        self.entry.grid(row=0, column=2, padx=15, pady=10, sticky=E + W)

        self.InitUI()


    def InitUI(self):
        
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
        self.labelDoB       = Label(self.frame, text=u'Date of Birth (YYYY-MM-DD)')

        self.buttonAdd    = Button(self.frame, width=12,
                                   text=u'Add candidate',
                                   command=self.AddIdentifierEvent
                                  )
        self.buttonClear  = Button(self.frame, width=12,
                                   text=u'Clear fields',
                                   command=self.clear
                                  )
        self.buttonSearch = Button(self.frame, width=12,
                                   text=u'Search candidate',
                                   command=self.search
                                  )
        self.buttonEdit   = Button(self.frame, width=12,
                                   text=u'Edit candidate',
                                   command=self.edit
                                  )

        self.textCandId  = StringVar()
        self.candidateid = Entry(self.frame,
                                 textvariable=self.textCandId,
                                 width=20
                                )
        self.candidateid.focus_set()

        self.textCandFirstName  = StringVar()
        self.candidateFirstName = Entry( self.frame,
                                         textvariable=self.textCandFirstName,
                                         width=20
                                       )

        self.textCandLastName  = StringVar()
        self.candidateLastName = Entry( self.frame,
                                        textvariable=self.textCandLastName,
                                        width=20
                                      )

        self.textCandDoB  = StringVar()
        self.candidateDoB = Entry(self.frame,
                                  textvariable=self.textCandDoB,
                                  width=20
                                 )

        self.tableColumns = ( "Identifier", "First Name",
                              "Last Name",  "Date of Birth"
                            )
        self.datatable    = ttk.Treeview(self.frame,
                                         selectmode='browse',
                                         columns=self.tableColumns,
                                         show="headings")
        for col in self.tableColumns:
            self.datatable.heading( col, text=col.title(),
                                    command=lambda c=col: sortby(self.datatable,
                                                                 c,
                                                                 0
                                                                )
                                  )

        self.datatable.bind("<<TreeviewSelect>>", self.OnRowClick)
      
        self.ErrorMessage = StringVar()
        self.error = Label(self.frame, textvariable=self.ErrorMessage, fg='red')

        self.labelID.grid(       row=0, column=0, padx=(0,4), sticky=E+W)
        self.labelFirstName.grid(row=0, column=1, padx=(4,4), sticky=E+W)
        self.labelLastName.grid( row=0, column=2, padx=(4,4), sticky=E+W)
        self.labelDoB.grid(      row=0, column=3, padx=(4,4), sticky=E+W)

        self.candidateid.grid( row=1,      column=0,
                               padx=(0,4), pady=(0,10),
                               sticky=E+W
                             )
        self.candidateFirstName.grid( row=1,      column=1,
                                      padx=(4,4), pady=(0,10),
                                      sticky=E+W
                                    )
        self.candidateLastName.grid( row=1,      column=2,
                                     padx=(4,4), pady=(0,10),
                                     sticky=E+W
                                   )
        self.candidateDoB.grid( row=1,      column=3,
                                padx=(4,4), pady=(0,10),
                                sticky=E+W
                              )
 
        self.buttonClear.grid( row=2, column=0, padx=(4,0), sticky=E+W)
        self.buttonSearch.grid(row=2, column=1, padx=(4,0), sticky=E+W)
        self.buttonEdit.grid(  row=2, column=2, padx=(4,0), sticky=E+W)
        self.buttonAdd.grid(   row=2, column=3, padx=(4,0), sticky=E+W)

        self.datatable.grid(row=3, column=0, columnspan=4, pady=10, sticky='nsew')
        self.error.grid(    row=4, column=0)


    def LoadXML(self):
        global data

        # empty the datatable and data dictionary before loading new file
        self.datatable.delete(*self.datatable.get_children())
        self.IDMap = {}

        """Parses the XML file and loads the data into the current window"""
        try:
            data = DataManagement.read_candidate_data()
            for key in data:
                identifier = data[key]["Identifier"]
                firstname  = data[key]["FirstName"]
                lastname   = data[key]["LastName"]
                dob = data[key]["DateOfBirth"]
                self.AddIdentifierAction( identifier, firstname,
                                          lastname,   dob,
                                          False
                                        )
        except Exception as e:
            print str(e)  #TODO add error login (in case a candidate data file does not exist)


    def AddIdentifierEvent(self):
        
        firstname = self.candidateFirstName.get()
        lastname  = self.candidateLastName.get()
        candid    = self.candidateid.get()
        dob       = self.candidateDoB.get()
        self.AddIdentifierAction(candid, firstname, lastname, dob)


    def AddIdentifierAction(self, candid, firstname, lastname, dob, save=True):
        """
        Adds the given identifier and real name to the mapping. If
        the "save" parameter is true, this also triggers the saving
        of the XML file. 
        This is set to False on initial load.
        """
        self.ErrorMessage.set("")

        # check that all fields are set
        if not candid or not firstname or not lastname or not dob:
            message = "ERROR:\nAll fields are\nrequired to add\na candidate"
            self.ErrorMessage.set(message)
            return

        # check candid does not already exist
        if candid in self.IDMap:
            message = "ERROR:\nCandidate ID\nalready exists"
            self.ErrorMessage.set(message)
            return

        # check dob is in format YYYY-MM-DD
        try:
            datetime.datetime.strptime(dob,"%Y-%m-%d")
        except ValueError:
            message = "ERROR:\nDate of birth's\nformat should be\n'YYYY-MM-DD'"
            self.ErrorMessage.set(message)
            return

        mapList = [candid, firstname, lastname, dob]
        self.IDMap[candid] = mapList
                        
        insertedList = [(candid, firstname, lastname, dob)]
        for item in insertedList:
            self.datatable.insert('', 'end', values=item)
        
        if(save):
            cand_data = {}
            cand_data["Identifier"]  = candid
            cand_data["FirstName"]   = firstname
            cand_data["LastName"]    = lastname
            cand_data["DateOfBirth"] = dob
            #self.SaveMapAction()
            DataManagement.save_candidate_data(cand_data)


    def OnRowClick(self, event):
        
        """Update the text boxes' data on row click"""
        item_id = str(self.datatable.focus())
        item = self.datatable.item(item_id)['values']
        
        self.textCandId.set(item[0])
        self.textCandFirstName.set(item[1])
        self.textCandLastName.set(item[2])
        self.textCandDoB.set(item[3])


    def clear(self):
        
        self.textCandId.set("")
        self.textCandFirstName.set("")
        self.textCandLastName.set("")
        self.textCandDoB.set("")
        self.candidateid.focus_set()


    def search(self):
        #  Find a candidate based on its ID if it is set in text box
        if self.textCandId.get():
            (candid,   firstname,
             lastname, dob) = self.FindCandidate( "candid",
                                                  self.textCandId.get()
                                                )
        # or based on its name if it is set in text box
        elif self.textCandFirstName.get():
            (candid,   firstname,
             lastname, dob) = self.FindCandidate( "firstname",
                                                  self.textCandFirstName.get()
                                                )
        elif self.textCandLastName.get():
            (candid,   firstname,
             lastname, dob) = self.FindCandidate( "lastname",
                                                  self.textCandLastName.get()
                                                )

        # print the values in the text box
        self.textCandId.set(candid)
        self.textCandFirstName.set(firstname)
        self.textCandLastName.set(lastname)
        self.textCandDoB.set(dob)


    def FindCandidate(self, key, value):
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
        self.EditIdentifierAction(self.textCandId.get(),
                                  self.textCandFirstName.get(),
                                  self.textCandLastName.get(),
                                  self.textCandDoB.get()
                                 )


    def EditIdentifierAction(self, identifier, firstname, lastname, dob, edit=True):

        # save data in the XML file
        cand_data = {}
        cand_data["Identifier"]  = identifier
        cand_data["FirstName"]   = firstname
        cand_data["LastName"]    = lastname
        cand_data["DateOfBirth"] = dob
        DataManagement.save_candidate_data(cand_data)

        # update the IDMap dictionary
        mapList = [identifier, firstname, lastname, dob]
        self.IDMap[identifier] = mapList

        # update datatable
        item = self.datatable.selection()
        updatedList = (identifier, firstname, lastname, dob)
        self.datatable.item(item, values=updatedList)


    def openfilename(self):

        """Returns a selected file name."""
        self.filename = tkFileDialog.askopenfilename(
            filetypes=[("XML files", "*.xml")]
        )
        self.entryVariable.set(self.filename)

        if self.filename:
            # Load the data
            Config.xmlfile = self.filename
            self.LoadXML()

        return self.filename


    def createfilename(self):

        self.filename = tkFileDialog.asksaveasfilename(
            defaultextension=[("*.xml")],
            filetypes=[("XML files", "*.xml")]
        )
        self.entryVariable.set(self.filename)

        if self.filename:
            open(self.filename, 'w')

            # Load the data
            Config.xmlfile = self.filename
            self.LoadXML()

        return self.filename

def main():
       
    root = Tk()
    app = IDMapper_frame_gui(root)
    root.mainloop()
 

if __name__ == "__main__":
    main()
