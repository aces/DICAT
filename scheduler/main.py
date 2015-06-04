#!/usr/bin/env python

from Tkinter import Tk
import userinterface


root = Tk()
app = userinterface.ApplicationGUI(root)
root.protocol("WM_DELETE_WINDOW", app.quitapplication)
app.mainloop()
