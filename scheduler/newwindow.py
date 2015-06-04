#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import packages
from Tkinter import *
#import functools
import dialogbox
import lib.utilities as utilities
import lib.multilanguage as multilanguage
import lib.datamanagement as datamanagement




#ref: http://effbot.org/tkinterbook/tkinter-newDialog-windows.htm
#TODO this class needs a major clean-up    
class NewWindow(Toplevel):
    def __init__(self, parent, candidate, function, visitlabel):  #TODO change for multilanguage variable
        Toplevel.__init__(self, parent)
        #create a transient window on top of parent window
        print "running NewWindow(Toplevel) " + str(candidate) + str(function) + str(visitlabel)  #TODO remove when done
        self.transient(parent) 
        self.parent = parent
        if function == 'schedule':
            self.title(multilanguage.schedulewindow_title)
        elif function == 'candidate':
            self.title(multilanguage.candidatewindow_title)
        body = Frame(self)
        self.initial_focus = self.body(body, candidate, function, visitlabel)
        body.pack(padx=5, pady=5)
        
        self.buttonbox()
        self.grab_set()
        
        if not self.initial_focus:
            self.initial_focus = self
            
        self.protocol("WM_DELETE_WINDOW", self.closedialog)
        
        utilities.centerwindow(self)   
        self.initial_focus.focus_set()

        self.deiconify()
        self.wait_window(self)


    def body(self, master, candidate, function, visitlabel):
        db = dict(datamanagement.readcandidatedata())
        candidate = db.get(candidate)        
        name = str(candidate.firstname) + " " + str(candidate.lastname)
        namelabel = Label(self, text = name)
        namelabel.pack(side=TOP, expand=YES, fill=BOTH)    
        if function == "schedule":
            currentvisitset = candidate.visitset
            currentvisit = currentvisitset.get(visitlabel)
            when = currentvisit.when
            where = currentvisit.where
            whenlabel = Label(self, text = when)
            whenlabel.pack(side=TOP, expand=YES, fill=BOTH)  
            wherelabel = Label(self, text = where)
            wherelabel.pack(side=TOP, expand=YES, fill=BOTH)  
        elif function == "candidate":
            phone = candidate.phone
            pscid = candidate.pscid
            phonelabel = Label(self, text=phone)
            phonelabel.pack(side=TOP, expand=YES, fill=BOTH)
            pscidlabel = Label(self, text=pscid)
            pscidlabel.pack(side=TOP, expand=YES, fill=BOTH)
             
        else:
            pass
       
    
    
    
    def buttonbox(self):
        # add standard button box
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.okbutton, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancelbutton)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.okbutton)
        self.bind("<Escape>", self.closedialog)
        box.pack()

    def okbutton(self, event=None):
        print "saving data and closing"  #TODO remove when done
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.closedialog()
        
    def cancelbutton(self, event=None):
        print "close without saving"
        parent = Frame(self)
        newwin = dialogbox.ConfirmYesNo(parent, multilanguage.dialogclose)
        if newwin.buttonvalue == 1:
            self.closedialog()
        else:
            return
        
    def closedialog(self, event=None):
        #put focus back to parent window before destroying the window
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        return 1  
