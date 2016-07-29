#import standard packages
from Tkinter import *

#import internal packages
import lib.utilities as Utilities
import lib.multilanguage as MultiLanguage

class DialogBox(Toplevel):
    """
    This class was created mainly because the native dialog box don't work as
    expected when called from a top-level window.
    This class (although it could be improved in many aspects) insure that the
    parent window cannot get focus while a dialog box is still active.

    """

    def __init__(self,parent, title, message, button1, button2):
        """
        Initialize the dialog box window.

        :param parent:  parent window to the dialog window
         :type parent:  object
        :param title:   title to give to the dialog window
         :type title:   str
        :param message: message to be displayed in the dialog window
         :type message: str
        :param button1: what should be written on button 1 of the dialog window
         :type button1: str
        :param button2: what should be written on button 2 of the dialog window
         :type button2: str

        """

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
        Utilities.center_window(self)
        self.initial_focus.focus_set()
        self.deiconify()
        self.wait_window(self)


    def body(self, parent, message):
        """
        Draw the body of the dialog box

        :param parent:  parent window of the dialog box
         :type parent:  object
        :param message: message to be drawn on the dialog box
         :type message: str

        """

        # Draw the message in the dialog box
        label = Label(self, text=message)
        label.pack(padx=4, pady=4)


    def buttonbox(self, button1, button2):
        """
        Draws the button box at the bottom of the dialog box.

        :param button1: button 1 of the button box
         :type button1: str
        :param button2: button 2 of the button box
         :type button2: str

        """

        #add a standard button box
        box = Frame(self)
        b1  = Button(
            box, text=button1, width=12, command=self.button1, default=ACTIVE
        )
        b1.pack(side=LEFT, padx=4, pady=4)
        self.bind("<Return>", self.button1)
        if button2:
            b2 = Button(
                box, text=button2, width=12, command=self.button2,
                default=ACTIVE
            )
            b2.pack(side=LEFT, padx=4, pady=4)
            self.bind("<Escape>", self.button2)
        box.pack()


    def button1(self, event=None):
        """
        Event handler for button1.

        :param event:
         :type event:

        """

        if not self.validate():
            self.initial_focus.focus_set() #put focus on Button
            return
        self.buttonvalue = 1
        self.closedialog()


    def button2(self, event=None):
        """
        Event handler for button2.

        :param event:
         :type event:

        """
        self.buttonvalue = 2
        self.closedialog()
        
        
    def closedialog(self, event=None):
        """
        Event handler to close the dialog box.

        :param event:
         :type event:

        """

        #put focus back to parent window before destroying the window
        self.parent.focus_set()
        self.destroy()


    def validate(self):
        return 1
        



class ConfirmYesNo(DialogBox):
    """
    Confirmation on closing a window class -> Yes or No.

    """

    def __init__(self, parent, message):
        """
        Initialization of the confirmation window class.

        :param parent:  parent of the confirmation window
         :type parent:  object
        :param message: message to print in the confirmation window.
         :type message: str

        """
        title   = MultiLanguage.dialog_title_confirm
        button1 = MultiLanguage.dialog_yes
        button2 = MultiLanguage.dialog_no
        DialogBox.__init__(self, parent, title, message, button1, button2)




class ErrorMessage(DialogBox):
    """
    Error Message pop up window.

    """

    def __init__(self, parent, message):
        """
        Initialization of the error message window.

        :param parent:  parent of the error message window to be displayed
         :type parent:  object
        :param message: message to be displayed on the error window.
         :type message: str

        """

        title  = MultiLanguage.dialog_title_error
        button = MultiLanguage.dialog_ok
        DialogBox.__init__(self, parent, title, message, button, None)
