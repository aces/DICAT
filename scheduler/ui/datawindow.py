#import standard packages
from Tkinter import *
from ttk import *
#import internal packages
from visit import Visit
import ui.dialogbox as DialogBox
import lib.utilities as Utilities
import lib.multilanguage as MultiLanguage
import lib.datamanagement as DataManagement

#ref: http://effbot.org/tkinterbook/tkinter-newDialog-windows.htm
#TODO this class needs a major clean-up    
class DataWindow(Toplevel):
    def __init__(self, parent, candidate_uuid):
        Toplevel.__init__(self, parent)
        #create a transient window on top of parent window
        print "running DataWindow(Toplevel) " + str(candidate_uuid)  #TODO remove when done
        self.transient(parent) 
        self.parent = parent
        self.title(MultiLanguage.data_window_title)  #TODO find a better title for the thing
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
        try:
            data = dict(DataManagement.read_candidate_data()) #TODO better way to do this
            candidate = data.get(candidate)
        except Exception as e:
            print str(e) #TODO manage exceptions
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

        #Schedule Section - displayed as a table
        self.schedule_pane = Labelframe(self, text=MultiLanguage.schedule_pane, width=250, height=350, borderwidth=10)
        self.schedule_pane.pack(side=TOP, expand=YES, fill=BOTH, padx=5, pady=5)
        #top row (header)
        self.label_visit_rank = Label(self.schedule_pane, text=MultiLanguage.schedule_visit_rank)
        self.label_visit_rank.grid(column=0, row=0, padx=5, pady=5, sticky=N+S+E+W)
        self.label_visit_label = Label(self.schedule_pane, text=MultiLanguage.col_visitlabel)
        self.label_visit_label.grid(column=1, row=0, padx=5, pady=5, sticky=N+S+E+W)
        self.label_visit_when = Label(self.schedule_pane, text=MultiLanguage.col_when)
        self.label_visit_when.grid(column=2, row=0, padx=5, pady=5, sticky=NSEW)
        self.label_visit_status = Label(self.schedule_pane, text=MultiLanguage.col_where)
        self.label_visit_status.grid(column=3, row=0, padx=5, pady=5, sticky=N+S+E+W)
        self.label_visit_status = Label(self.schedule_pane, text=MultiLanguage.col_withwhom)
        self.label_visit_status.grid(column=4, row=0, padx=5, pady=5, sticky=N+S+E+W)
        self.label_visit_status = Label(self.schedule_pane, text=MultiLanguage.col_status)
        self.label_visit_status.grid(column=5, row=0, padx=5, pady=5, sticky=N+S+E+W)

        """
        PSEUDOCODE
        1. Get candidate.visitset
        2. Parse into a sorted (on visit.rank) list
        3. Print data on scree


        visit_set = candidate.visitset
        for key, value in study_setup.iteritems():
            visit_list.append(study_setup[key])
        visit_list = sorted(visit_list, key=lambda visit: visit.rank)

        for key, value in visit_list.iteritems():

        """
        #TODO add logic "foreach" to create a table showing each visit
        import lib.utilities as Utilities #TODO delete when done
        #1- Get candidate visitset and parse into a list
        visit_list = []
        visitset = candidate.visitset
        if visitset is None:
            print 'no visit yet'
        else:
            for key, value in visitset.iteritems():
                visit_list.append(visitset[key])
            #2- Sort list on visit.rank
            visit_list = sorted(visit_list, key=lambda visit: visit.rank)
            #3- 'print' values on ui
            import lib.entrybox as EntryBox  #TODO relocate when done
            x = 0
            for x in range(len(visit_list)):
                #rank
                label_visit_rank = Label(self.schedule_pane, text=visit_list[x].rank)
                label_visit_rank.grid(column=0, row=x+1, padx=5, pady=5, sticky=N+S+E+W)
                #visitlabel
                label_visit_label = Label(self.schedule_pane, text=visit_list[x].visitlabel)
                label_visit_label.grid(column=1, row=x+1, padx=5, pady=5, sticky=N+S+E+W)
                #when
                if visit_list[x].when == None:
                    visit = visit_list[x]
                    date_range = Visit.visit_date_range(visit)
                    print date_range
                    label_visit_when = Label(self.schedule_pane, text=date_range)
                    label_visit_when.grid(column=2, row=x+1, padx=5, pady=5, sticky=N+S+E+W)
                else:
                    label_visit_when = Label(self.schedule_pane, text=visit_list[x].when)
                    label_visit_when.grid(column=2, row=x+1, padx=5, pady=5, sticky=N+S+E+W)
                #where
                label_visit_where = Label(self.schedule_pane, text=visit_list[x].where)
                label_visit_where.grid(column=3, row=x+1, padx=5, pady=5, sticky=N+S+E+W)
                #withwhom
                label_visit_where = Label(self.schedule_pane, text=visit_list[x].withwhom)
                label_visit_where.grid(column=4, row=x+1, padx=5, pady=5, sticky=N+S+E+W)
                #status
                label_visit_where = Label(self.schedule_pane, text=visit_list[x].status)
                label_visit_where.grid(column=5, row=x+1, padx=5, pady=5, sticky=N+S+E+W)



    def button_box(self):
        # add standard button box
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok_button, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel_button)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok_button)
        self.bind("<Escape>", self.closedialog)
        box.pack()

    def ok_button(self, event=None):
        print "saving data and closing"  #TODO remove when done
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
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
        self.parent.focus_set() #put focus back to parent window before destroying the window
        self.destroy()

    def validate(self):
        return 1
