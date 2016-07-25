#import standard packages
from Tkinter import *
from ttk import *
#import internal packages
import ui.dialogbox as DialogBox
import lib.utilities as Utilities
import lib.multilanguage as MultiLanguage
import lib.datamanagement as DataManagement

class NewCandidateWindow(TopLevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        #create a transient window on top of parent window
        print "running NewCandidate(Toplevel) " #TODO remove when done
        self.transient(parent)
        self.parent = parent
        self.title(MultiLanguage.new_candidate_title)
        body = Frame(self)
        self.initial_focus = self.body(body, candidate_uuid)
        body.pack(padx=5, pady=5)

        self.button_box()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.closedialog)
        Utilities.center_window(self)
        self.initial_focus.focus_set()
        #self.deiconify()
        self.wait_window(self)

    def body(self, master, candidate):
        #Candidate section
        self.candidate_pane = Labelframe(self, text=MultiLanguage.candidate_pane, width=250, height=350, borderwidth=10)
        self.candidate_pane.pack(side=TOP, expand=YES, fill=BOTH, padx=5, pady=5)
        #PSCID
        self.label_pscid = Label(self.candidate_pane, text=MultiLanguage.candidate_pscid)
        self.label_pscid.grid(column=0, row=0, padx=10, pady=5, sticky=N+S+E+W)
        self.text_pscid_var = StringVar()
        self.text_pscid_var.set(candidate.pscid)
        self.text_pscid = Entry(self.candidate_pane, textvariable=self.text_pscid_var)
        self.text_pscid.grid(column=0, row=1, padx=10, pady=5, sticky=N+S+E+W)
        #status
        self.label_status = Label(self.candidate_pane, text=MultiLanguage.candidate_status)
        self.label_status.grid(column=1, row=0, padx=10, pady=5, sticky=N+S+E+W)
        self.text_status_var = StringVar()
        self.text_status_var.set(candidate.status)
        self.text_status = Entry(self.candidate_pane, textvariable=self.text_status_var)
        self.text_status.grid(column=1, row=1, padx=10, pady=5, sticky=N+S+E+W)
        #firstname
        self.label_firstname = Label(self.candidate_pane, text=MultiLanguage.candidate_firstname)
        self.label_firstname.grid(column=0, row=2, padx=10, pady=5, sticky=N+S+E+W)
        self.text_firstname_var = StringVar()
        self.text_firstname_var.set(candidate.firstname)
        self.text_firstname = Entry(self.candidate_pane, textvariable=self.text_firstname_var)
        self.text_firstname.grid(column=0, row=3, padx=10, pady=5, sticky=N+S+E+W)
        #lastname
        self.label_lastname = Label(self.candidate_pane, text=MultiLanguage.candidate_lastname)
        self.label_lastname.grid(column=1, row=2, padx=10, pady=5, sticky=N+S+E+W)
        self.text_lastname_var = StringVar()
        self.text_lastname_var.set(candidate.lastname)
        self.text_lastname = Entry(self.candidate_pane, textvariable=self.text_lastname_var)
        self.text_lastname.grid(column=1, row=3, padx=10, pady=5, sticky=N+S+E+W)
        #phone number
        self.label_phone = Label(self.candidate_pane, text=MultiLanguage.candidate_phone)
        self.label_phone.grid(column=2, row=2, padx=10, pady=5, sticky=N+S+E+W)
        self.text_phone_var = StringVar()
        self.text_phone_var.set(candidate.phone)
        self.text_phone = Entry(self.candidate_pane, textvariable=self.text_phone_var)
        self.text_phone.grid(column=2, row=3, padx=10, pady=5, sticky=N+S+E+W)
        #pscid
        #self.label_pscid = Label(self.candidate_pane, textvariable=self.pscid_var)

         
