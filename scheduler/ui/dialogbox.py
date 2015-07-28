#import standard packages
from Tkinter import *
#import internal packages
import lib.utilities as Utilities
import lib.multilanguage as MultiLanguage

class DialogBox(Toplevel):
    """
    This class was created mainly because the native dialog box don't work as expected when called from a top-level window.
    This class (although it could be improved in many aspects) insure that the parent window cannot get focus while a dialog box is still active.
    """
    def __init__(self,parent, title, message, button_ok, button_cancel):
        Toplevel.__init__(self,parent)
        self.transient(parent)
        self.parent = parent
        self.title(title)
        body = Frame(self)
        self.initial_focus = self.body(body, message)
        body.pack(padx=4, pady=4)
        self.buttonbox(button_ok, button_cancel)
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self
        
        self.protocol("WM_DELETE_WINDOW", self.button_cancel)
        Utilities.center_window(self)
        self.initial_focus.focus_set()
        self.deiconify()
        self.wait_window(self)
        
    def body(self, parent, message):
        label = Label(self, text=message)
        label.pack(padx=4, pady=4)
        pass
      
    def buttonbox(self, button_ok, button_cancel):
        #add a standard button box
        box = Frame(self)
        b1 = Button(box, text=button_ok, width=12, command=self.button_ok, default=ACTIVE)
        b1.pack(side=LEFT, padx=4, pady=4)
        b2 = Button(box, text=button_cancel, width=12, command=self.button_cancel, default=ACTIVE)
        b2.pack(side=LEFT, padx=4, pady=4)
        self.bind("<Return>", self.button_ok)
        self.bind("<Escape>", self.button_cancel)
        box.pack()
        
    def button_ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() #put focus on Button
            return
        self.buttonvalue = 1
        self.closedialog()
        
    def button_cancel(self, event=None):
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
        title = MultiLanguage.dialog_title_confirm
        button_yes = MultiLanguage.dialog_yes
        button_no  = MultiLanguage.dialog_no
        DialogBox.__init__(self, parent, title, message, button_yes, button_no)
    
    

        
