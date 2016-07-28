# import standard packages
from Tkinter import *
from ttk import *
# import internal packages
from scheduler_visit import Visit
import ui.dialogbox as DialogBox
import lib.utilities as Utilities
import lib.multilanguage as MultiLanguage
import lib.datamanagement as DataManagement
from lib.candidate import Candidate


# ref: http://effbot.org/tkinterbook/tkinter-newDialog-windows.htm
# TODO this class needs a major clean-up


class DataWindow(Toplevel):

    def __init__(self, parent, candidate=False):
        """
        Initialize the DataWindow class.

        :param parent: parent frame of the data window
         :type parent: object
        :param candidate: candidate ID or 'new' for a new candidate
         :type candidate: str

        """

        Toplevel.__init__(self, parent)

        # Create a transient window on top of parent window
        self.transient(parent)
        self.parent    = parent
        self.candidate = candidate
        #TODO find a better title for the data window
        self.title(MultiLanguage.data_window_title)
        body = Frame(self)

        # Draw the body of the data window
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        # Draw the button box of the data window
        self.button_box()

        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.closedialog)
        Utilities.center_window(self)
        self.initial_focus.focus_set()
        self.wait_window(self)


    def body(self, master):
        """
        Creates the body of the 'datawindow'.

        :param master: frame in which to draw the body of the datawindow
         :type master: object
        :param candidate: candidate ID or 'new' for a new candidate
         :type candidate: str

        """

        try:
            # Read candidate information
            cand_data  = DataManagement.read_candidate_data()
            # Read visit information
            visit_data = DataManagement.read_visitset_data()
            visitset   = {}   # Create a visitset dictionary
            cand_info  = {}   # Create a candidate information dictionary

            # Loop through all candidates
            for cand_key in cand_data:
                # Grep candidate's information from cand_data dictionary
                if cand_data[cand_key]["Identifier"] == self.candidate:
                    cand_info = cand_data[cand_key]
                    break

            # Loop through candidates' visit data
            for cand_key in visit_data:
                # Grep candidate's visit set information from visit_data
                if visit_data[cand_key]["Identifier"] == self.candidate:
                    visitset = visit_data[cand_key]["VisitSet"]
                    break

        except Exception as e:
            print "datawindow.body ", str(e)  # TODO manage exceptions

        ## Candidate section
        self.candidate_pane = Labelframe( self,
                                          text=MultiLanguage.candidate_pane,
                                          width=250,
                                          height=350,
                                          borderwidth=10
                                        )
        self.candidate_pane.pack( side=TOP, expand=YES, fill=BOTH,
                                  padx=5,   pady=5
                                )

        # Initialize text variables that will contain the field values
        self.text_pscid_var     = StringVar()
        self.text_firstname_var = StringVar()
        self.text_lastname_var  = StringVar()
        self.text_dob_var       = StringVar()
        self.text_gender_var    = StringVar()
        self.text_status_var    = StringVar()
        self.text_phone_var     = StringVar()

        # If candidate is populated with candID populate the fields with values
        # available in cand_info dictionary, otherwise populate with empty str
        if self.candidate:
            self.text_pscid_var.set(cand_info["Identifier"])
            self.text_firstname_var.set(cand_info["FirstName"])
            self.text_lastname_var.set(cand_info["LastName"])
            self.text_dob_var.set(cand_info["DateOfBirth"])
            self.text_gender_var.set(cand_info["Gender"])
            self.text_status_var.set(cand_info["CandidateStatus"])
            self.text_phone_var.set(cand_info["PhoneNumber"])
        else:
            self.text_pscid_var.set("")
            self.text_firstname_var.set("")
            self.text_lastname_var.set("")
            self.text_dob_var.set("")
            self.text_gender_var.set(" ")
            self.text_status_var.set(" ")
            self.text_phone_var.set("")

        # Create widgets to be displayed
        # (typically a label with a text box underneath per variable to display)
        self.label_pscid = Label(     # identifier label
            self.candidate_pane, text=MultiLanguage.candidate_pscid
        )
        self.text_pscid  = Entry(     # identifier text box
            self.candidate_pane, textvariable=self.text_pscid_var
        )
        self.label_firstname = Label( # firstname label
            self.candidate_pane, text=MultiLanguage.candidate_firstname
        )
        self.text_firstname  = Entry( # firstname text box
            self.candidate_pane, textvariable=self.text_firstname_var
        )
        self.label_lastname = Label(  # lastname label
            self.candidate_pane, text=MultiLanguage.candidate_lastname
        )
        self.text_lastname  = Entry(  # lastname text box
            self.candidate_pane, textvariable=self.text_lastname_var
        )
        self.label_dob = Label(       # date of birth label
            self.candidate_pane, text=MultiLanguage.candidate_dob
        )
        self.text_dob  = Entry(       # date of birth text box
            self.candidate_pane, textvariable=self.text_dob_var
        )
        self.label_gender = Label(    # gender label
            self.candidate_pane, text=MultiLanguage.candidate_gender
        )
        gender_options = [' ', 'Male', 'Female']
        self.text_gender  = OptionMenu( # gender selected from a drop down menu
            self.candidate_pane,
            self.text_gender_var,  # variable in which to store the selection
            self.text_gender_var.get(), # default value to be used at display
            *gender_options             # list of drop down options
        )
        self.label_status = Label(    # candidate status label
            self.candidate_pane, text=MultiLanguage.candidate_status
        )
        #TODO: grep the status_options list from the project information
        status_options = [
            ' ',     'active',     'withdrawn', 'excluded',
            'death', 'ineligible', 'completed'
        ]
        self.text_status  = OptionMenu( # cand. status selected from drop down
            self.candidate_pane,
            self.text_status_var,  # variable in which to store the selection
            self.text_status_var.get(), # default value to be used at display
            *status_options             # list of drop down options
        )
        self.label_phone = Label(     # phone number label
            self.candidate_pane, text=MultiLanguage.candidate_phone
        )
        self.text_phone  = Entry(     # phone number text box
            self.candidate_pane, textvariable=self.text_phone_var
        )

        # Draw widgets in the candidate pane section
        self.label_pscid.grid(     # draw identifier label
            column=0, row=0, padx=10, pady=5, sticky=N+S+E+W
        )
        self.text_pscid.grid(      # draw identifier text box
            column=0, row=1, padx=10, pady=5, sticky=N+S+E+W
        )
        self.label_firstname.grid( # draw firstname label
            column=1, row=0, padx=10, pady=5, sticky=N+S+E+W
        )
        self.text_firstname.grid( # draw firstname text box
            column=1, row=1, padx=10, pady=5, sticky=N+S+E+W
        )
        self.label_lastname.grid( # draw lastname label
            column=2, row=0, padx=10, pady=5, sticky=N+S+E+W
        )
        self.text_lastname.grid(  # draw lastname text box
            column=2, row=1, padx=10, pady=5, sticky=N+S+E+W
        )
        self.label_dob.grid(      # draw date of birth label
            column=3, row=0, padx=10, pady=5, sticky=N+S+E+W
        )
        self.text_dob.grid(       # draw date of birth text box
            column=3, row=1, padx=10, pady=5, sticky=N+S+E+W
        )
        self.label_gender.grid(   # draw gender label
            column=0, row=2, padx=10, pady=5, sticky=N+S+E+W
        )
        self.text_gender.grid(    # draw gender text box
            column=0, row=3, padx=10, pady=5, sticky=N+S+E+W
        )
        self.label_status.grid(   # draw candidate status label
            column=1, row=2, padx=10, pady=5, sticky=N+S+E+W
        )
        self.text_status.grid(    # draw candidate status text box
            column=1, row=3, padx=10, pady=5, sticky=N+S+E+W
        )
        self.label_phone.grid(    # draw phone number label
            column=2, row=2, padx=10, pady=5, sticky=N+S+E+W
        )
        self.text_phone.grid(     # draw phone number text box
            column=2, row=3, padx=10, pady=5, sticky=N+S+E+W
        )


        ## Calendar Section - displayed as a table
        self.schedule_pane = Labelframe(
            self,          text=MultiLanguage.schedule_pane,
            width=250,     height=350,
            borderwidth=10
        )
        self.schedule_pane.pack(side=TOP, expand=YES, fill=BOTH, padx=5, pady=5)

        # top row (header)
        self.label_visit_label = Label(
            self.schedule_pane, text=MultiLanguage.col_visitlabel
        )
        self.label_visit_when = Label(
            self.schedule_pane, text=MultiLanguage.col_when
        )
        self.label_visit_label.grid(
            column=1, row=0, padx=5, pady=5, sticky=N+S+E+W
        )
        self.label_visit_when.grid(
            column=2, row=0, padx=5, pady=5, sticky=N+S+E+W
        )
        self.label_visit_status = Label(
            self.schedule_pane, text=MultiLanguage.col_where
        )
        self.label_visit_status.grid(
            column=3, row=0, padx=5, pady=5, sticky=N+S+E+W
        )
        self.label_visit_status = Label(
            self.schedule_pane, text=MultiLanguage.col_withwhom
        )
        self.label_visit_status.grid(
            column=4, row=0, padx=5, pady=5, sticky=N+S+E+W
        )
        self.label_visit_status = Label(
            self.schedule_pane, text=MultiLanguage.col_status
        )
        self.label_visit_status.grid(
            column=5, row=0, padx=5, pady=5, sticky=N+S+E+W
        )

        """
        PSEUDOCODE
        1. Get candidate.visitset
        2. Parse into a sorted list (sorted on visit.rank)
        3. Print cand_data on screen


        visit_set = candidate.visitset
        for key, value in study_setup.iteritems():
            visit_list.append(study_setup[key])
        visit_list = sorted(visit_list, key=lambda visit: visit.rank)

        for key, value in visit_list.iteritems():

        """
        # TODO add logic "foreach" to create a table showing each visit
        # 1- Get candidate visitset and parse into a list
        visit_list = []
        if len(visitset.keys()) == 0:
            print 'no visit yet'
        else:
            for key, value in visitset.iteritems():
                visit_list.append(visitset[key])

            # 2- Sort list on visit.rank
            visit_list = sorted( visit_list,
                                 key=lambda visit: visit["VisitStartWhen"]
                               )

            # 3- 'print' values on ui
            x = 0
            for x in range(len(visit_list)):
                # visitlabel
                label_visit_label = Label( self.schedule_pane,
                                           text=visit_list[x]["VisitLabel"]
                                         )
                label_visit_label.grid( column=1, row=x+1,
                                        padx=5,   pady=5,
                                        sticky=N+S+E+W
                                      )
                # when
                visit_when = ""
                if "VisitStartWhen" not in visit_list[x].keys():
                    #visit = visit_list[x]["VisitLabel"]
                    #date_range = visit.visit_date_range()
                    #TODO: implement automatic range for next visit
                    visit_when = ""
                else:
                    visit_when = visit_list[x]["VisitStartWhen"]
                label_visit_when = Label(self.schedule_pane, text=visit_when)
                label_visit_when.grid( column=2, row=x+1,
                                       padx=5,   pady=5,
                                       sticky=N+S+E+W
                                     )

                # where
                visit_where = ""
                if "VisitWhere" in visit_list[x].keys():
                    visit_where = visit_list[x]["VisitWhere"]
                label_visit_where = Label(self.schedule_pane, text=visit_where)
                label_visit_where.grid( column=3, row=x+1,
                                        padx=5,   pady=5,
                                        sticky=N+S+E+W
                                      )

                # withwhom
                visit_with_whom = ""
                if "VisitWithWhom" in visit_list[x].keys():
                    visit_with_whom = visit_list[x]["VisitWithWhom"]
                label_visit_with_whom = Label( self.schedule_pane,
                                               text=visit_with_whom
                                             )
                label_visit_with_whom.grid( column=4, row=x+1,
                                            padx=5,   pady=5,
                                            sticky=N+S+E+W
                                          )

                # status
                visit_status = ''
                if "VisitStatus" in visit_list[x].keys():
                    visit_status = visit_list[x]["VisitStatus"]
                label_visit_status = Label( self.schedule_pane,
                                            text=visit_status
                                          )
                label_visit_status.grid( column=5, row=x+1,
                                         padx=5,   pady=5,
                                         sticky=N+S+E+W
                                       )


    def button_box(self):

        # add standard button box
        box = Frame(self)

        # description_frame_gui buttons
        ok = Button( box,      text="OK",
                     width=10, command=self.ok_button,
                     default=ACTIVE
                   )
        cancel = Button( box,      text="Cancel",
                         width=10, command=self.cancel_button
                       )

        # draw the buttons
        ok.pack(side=LEFT, padx=5, pady=5)
        cancel.pack(side=LEFT, padx=5, pady=5)

        # bind key handlers to button functions
        self.bind("<Return>", self.ok_button)
        self.bind("<Escape>", self.closedialog)

        # draw the button box
        box.pack()


    def ok_button(self, event=None):

        message = self.capture_data()

        if message:
            parent = Frame(self)
            newwin = DialogBox.ErrorMessage(
                        parent,
                        message
            )
            if newwin.buttonvalue == 1:
                return # to stay on the candidate pop up page after clicking OK

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        #need to call treeview update here
        self.withdraw()
        self.closedialog()


    def cancel_button(self, event=None):
        print "close without saving"
        parent = Frame(self)
        newwin = DialogBox.ConfirmYesNo(parent, MultiLanguage.dialog_close)
        if newwin.buttonvalue == 1:
            self.closedialog()
        else:
            return


    def closedialog(self, event=None):
        # put focus back to parent window before destroying the window
        self.parent.focus_set()
        self.destroy()


    def validate(self):
        return 1


    def capture_data(self):
        """
        Grep the information from the pop up window's text fields and save the
        candidate information based on the pscid.

        :param: None

        :return: None

        """

        # Initialize the candidate dictionary with new values
        cand_data = {}

        # Capture data from fields
        cand_data['Identifier']  = self.text_pscid.get()
        cand_data['FirstName']   = self.text_firstname.get()
        cand_data['LastName']    = self.text_lastname.get()
        cand_data['DateOfBirth'] = self.text_dob.get()
        cand_data['Gender']      = self.text_gender_var.get()
        cand_data['PhoneNumber'] = self.text_phone.get()
        cand_data['CandidateStatus'] = self.text_status_var.get()

        # Set CandidateStatus to space string if not defined in cand_data
        if not cand_data['CandidateStatus']:
            cand_data['CandidateStatus'] = " "

        # Set PhoneNumber to space string if not defined in cand_data
        if not cand_data['PhoneNumber']:
            cand_data['PhoneNumber']     = " "

        # Check fields format and required fields
        candidate = Candidate(cand_data)
        message = candidate.check_candidate_data('scheduler', self.candidate)
        if message:
            return message

        # Save candidate data
        DataManagement.save_candidate_data(cand_data)
