#import packages
from Tkinter import *
import functools
import lib.utilities as utilities
import lib.multilanguage as multilanguage

class DialogBox(Toplevel):
    """
    This class was created mainly because the native dialog box don't work as expected when called from a top-level window.
    This class (although it could be improved in many aspects) insure that the parent window cannot get focus while this dialog box is still active.
    """
    def __init__(self,parent, title, message, button1, button2):
        Toplevel.__init__(self,parent)
        self.transient(parent)
        self.parent = parent
        self.title(title)
        
        body = Frame(self)
        self.initial_focus = self.body(body, message)
        body.pack(padx=4, pady=4)
        
        self.buttonbox(button1, button2)
        self.grab_set()
        
        if not self.initial_focus:
            self.initial_focus = self
        
        self.protocol("WM_DELETE_WINDOW", self.button2)
        utilities.centerwindow(self)
        self.initial_focus.focus_set()
        self.deiconify()
        self.wait_window(self)
        
    def body(self, parent, message):
        label = Label(self, text=message)
        label.pack(padx=4, pady=4)
        pass
      
    def buttonbox(self, button1, button2):
        #add a standard button box
        box = Frame(self)
        b1 = Button(box, text=button1, width=12, command=self.button1, default=ACTIVE)
        b1.pack(side=LEFT, padx=4, pady=4)
        b2 = Button(box, text=button2, width=12, command=self.button2, default=ACTIVE)
        b2.pack(side=LEFT, padx=4, pady=4)
        self.bind("<Return>", self.button1)
        self.bind("<Escape>", self.button2)
        box.pack()
        
    def button1(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() #put focus on Button
            return
        self.buttonvalue = 1
        self.closedialog()
        
    def button2(self, event=None):
        self.buttonvalue = 2
        self.closedialog()
        
        
    def closedialog(self, event=None):
        #put focus back to parent window before destroying the window
        self.parent.focus_set()
        self.destroy()
        
    def validate(self):
        return 1
        
#########################################################################################        
class ConfirmYesNo(DialogBox):
    def __init__(self, parent, message):
        title = multilanguage.dialogtitle_confirm
        button1 = multilanguage.dialog_yes
        button2 = multilanguage.dialog_no
        DialogBox.__init__(self, parent, title, message, button1, button2)
    
    

        
