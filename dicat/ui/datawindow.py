# import standard packages
from Tkinter import *
from ttk import *
# import internal packages
import ui.dialogbox as DialogBox
import lib.utilities as Utilities
import lib.multilanguage as MultiLanguage
import lib.datamanagement as DataManagement
from lib.candidate import Candidate


# ref: http://effbot.org/tkinterbook/tkinter-newDialog-windows.htm
# TODO this class needs a major clean-up


class DataWindow(Toplevel):

    def __init__(self, parent, candidate=''):
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
        self.protocol("WM_DELETE_WINDOW", self.close_dialog)
        Utilities.center_window(self)
        self.initial_focus.focus_set()
        self.wait_window(self)


    def body(self, master):
        """
        Creates the body of the 'data window'.

        :param master: frame in which to draw the body of the data window
         :type master: object

        """

        # Load the candidate and visitset data
        cand_info = []
        visitset  = []
        if not self.candidate == 'new':
            (cand_info, visitset) = self.load_data()

        ## Create a candidate section in the data window
        self.candidate_pane = Labelframe(
            self,
            text=MultiLanguage.candidate_pane,
            width=250,
            height=350,
            borderwidth=10
        )
        self.candidate_pane.pack(
            side=TOP, expand=YES, fill=BOTH, padx=5, pady=5
        )

        # Draw in the candidate section of the data window
        self.candidate_pane_ui(cand_info)

        # Draw the visit section if self.candidate is not 'new' or 'search'
        if not self.candidate == 'new':
            # Create a calendar section in the data window
            self.schedule_pane = Labelframe(
                self,
                text=MultiLanguage.schedule_pane,
                width=250,
                height=350,
                borderwidth=10
            )
            self.schedule_pane.pack(
                side=TOP, expand=YES, fill=BOTH, padx=5, pady=5
            )
            # Draw in the calendar section of the data window
            self.schedule_pane_ui(visitset)


    def candidate_pane_ui(self, cand_info):
        """
        Draws the candidate section of the datawindow and populates it fields
        based on what is store in cand_info

        :param cand_info: dictionary with the candidate's information
         :type cand_info: dict

        """

        # Initialize text variables that will contain the field values
        self.text_pscid_var     = StringVar()
        self.text_firstname_var = StringVar()
        self.text_lastname_var  = StringVar()
        self.text_dob_var       = StringVar()
        self.text_gender_var    = StringVar()
        self.text_status_var    = StringVar()
        self.text_phone_var     = StringVar()

        # If self.candidate is populated with a candID populate the fields with
        # values available in cand_info dictionary, otherwise populate with
        # empty str or " " in the case of drop down menus
        if self.candidate == 'new':
            self.text_pscid_var.set("")
            self.text_firstname_var.set("")
            self.text_lastname_var.set("")
            self.text_dob_var.set("")
            self.text_gender_var.set(" ")
            self.text_status_var.set(" ")
            self.text_phone_var.set("")
        else:
            self.text_pscid_var.set(cand_info["Identifier"])
            self.text_firstname_var.set(cand_info["FirstName"])
            self.text_lastname_var.set(cand_info["LastName"])
            self.text_dob_var.set(cand_info["DateOfBirth"])
            self.text_gender_var.set(cand_info["Gender"])
            self.text_status_var.set(cand_info["CandidateStatus"])
            self.text_phone_var.set(cand_info["PhoneNumber"])

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


    def schedule_pane_ui(self, visitset):

        # If the candidate has not visit set, display a message on the calendar
        # section to say that no visit has been scheduled yet for that candidate
        if not visitset:
            self.label_no_visit = Label(
                self.schedule_pane, text=MultiLanguage.schedule_no_visit_yet
            )
            self.label_no_visit.grid(
                row=0, column=1, columnspan=4, padx=5, sticky=N+S+E+W
            )
            return

        # Create top row (header) widgets
        self.label_visit_label = Label(     # create visit label widget
            self.schedule_pane, text=MultiLanguage.col_visitlabel
        )
        self.label_visit_when = Label(      # create visit when widget
            self.schedule_pane, text=MultiLanguage.col_when
        )
        self.label_visit_where = Label(     # create visit where widget
            self.schedule_pane, text=MultiLanguage.col_where
        )
        self.label_visit_withwhom = Label(  # create visit withwhom widget
            self.schedule_pane, text=MultiLanguage.col_withwhom
        )
        self.label_visit_status = Label(    # create visit status widget
            self.schedule_pane, text=MultiLanguage.col_status
        )

        # Draw the top row (header) widgets
        self.label_visit_label.grid(        # draw visit label widget
            row=0, column=1, padx=5, pady=5, sticky=N+S+E+W
        )
        self.label_visit_when.grid(         # draw visit when widget
            row=0, column=2, padx=5, pady=5, sticky=N+S+E+W
        )
        self.label_visit_where.grid(        # draw visit where widget
            row=0, column=3, padx=5, pady=5, sticky=N+S+E+W
        )
        self.label_visit_withwhom.grid(     # draw visit withwhom widget
            row=0, column=4, padx=5, pady=5, sticky=N+S+E+W
        )
        self.label_visit_status.grid(       # draw visit status widget
            row=0, column=5, padx=5, pady=5, sticky=N+S+E+W
        )

        # Sort visit list based on the VisitStartWhen field
        visit_list = DataManagement.sort_candidate_visit_list(visitset)

        # Show values on ui
        row_number=1
        for visit in visit_list:

            # Check if values are set for VisitStartWhen, VisitWhere,
            # VisitWindow & VisitStatus keys. If not, set it to empty string as
            # we need a text to display in the corresponding label widgets.
            visit_when   = ""
            visit_where  = ""
            visit_status = ""
            visit_with_whom = ""
            if "VisitStartWhen" in visit.keys():
                #TODO: implement automatic range for next visit
                visit_when = visit["VisitStartWhen"]
            if "VisitWhere" in visit.keys():
                visit_where = visit["VisitWhere"]
            if "VisitWithWhom" in visit.keys():
                visit_with_whom = visit["VisitWithWhom"]
            if "VisitStatus" in visit.keys():
                visit_status = visit["VisitStatus"]

            # Create the visit row widgets
            label_visit_label = Label(     # visit label widget
                self.schedule_pane, text=visit["VisitLabel"]
            )
            label_visit_when  = Label(     # visit when widget
                self.schedule_pane, text=visit_when
            )
            label_visit_where = Label(     # visit where widget
                self.schedule_pane, text=visit_where
            )
            label_visit_with_whom = Label( # visit with whom widget
                self.schedule_pane, text=visit_with_whom
            )
            label_visit_status = Label(    # visit status widget
                self.schedule_pane, text=visit_status
            )

            # Draw the visit row widget
            label_visit_label.grid(
                row=row_number+1, column=1, padx=5, pady=5, sticky=N+S+E+W
            )
            label_visit_when.grid(
                row=row_number+1, column=2, padx=5, pady=5, sticky=N+S+E+W
            )
            label_visit_where.grid(
                row=row_number+1, column=3, padx=5, pady=5, sticky=N+S+E+W
            )
            label_visit_with_whom.grid(
                row=row_number+1, column=4, padx=5, pady=5, sticky=N+S+E+W
            )
            label_visit_status.grid(
                row=row_number+1, column=5, padx=5, pady=5, sticky=N+S+E+W
            )

            # Increment row_number for the next visit to be displayed
            row_number += 1


    def load_data(self):
        """
        Read the XML data and return the candidate's (self.candidate)
        information as well as its visit information.

        :return cand_data:  data dictionary with candidate information
         :rtype cand_data:  dict
        :return visit_data: data dictionary with visit information
         :rtype visit_data: dict

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
                if visit_data[cand_key]["Identifier"] == self.candidate \
                        and 'VisitSet' in visit_data[cand_key]:
                    visitset = visit_data[cand_key]["VisitSet"]
                    break

        except Exception as e:
            print "datawindow.body ", str(e)  # TODO manage exceptions
            return

        return cand_info, visitset


    def button_box(self):
        """
        Draws the button box at the bottom of the data window.

        """

        # add standard button box
        box = Frame(self)

        # description_frame_gui buttons
        ok = Button(
            box, text="OK", width=10, command=self.ok_button, default=ACTIVE
        )
        cancel = Button(
            box, text="Cancel", width=10, command=self.cancel_button
        )

        # draw the buttons
        ok.pack(side=LEFT, padx=5, pady=5)
        cancel.pack(side=LEFT, padx=5, pady=5)

        # bind key handlers to button functions
        self.bind("<Return>", self.ok_button)
        self.bind("<Escape>", self.close_dialog)

        # draw the button box
        box.pack()


    def ok_button(self, event=None):
        """
        Event handler for the OK button. If something was missing in the data
        and it could not be saved, it will pop up an error message with the
        appropriate error message.

        :param event:
         :type event:

        :return:

        """

        message = self.capture_data()

        if message:
            parent = Frame(self)
            newwin = DialogBox.ErrorMessage(parent, message)
            if newwin.buttonvalue == 1:
                return # to stay on the candidate pop up page after clicking OK

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        #need to call treeview update here
        self.withdraw()
        self.close_dialog()


    def cancel_button(self, event=None):
        """
        Event handler for the cancel button. Will ask confirmation if want to
        cancel, if yes put focus back to the datatable without saving, else put
        focus back to the data window.

        :param event:
         :type event:

        :return:

        """

        parent = Frame(self)
        newwin = DialogBox.ConfirmYesNo(parent, MultiLanguage.dialog_close)
        if newwin.buttonvalue == 1:
            self.close_dialog()
        else:
            return


    def close_dialog(self, event=None):
        """
        Close dialog handler: will put focus back to the parent window.

        :param event:
        :return:

        """

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
