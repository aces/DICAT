#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter, Tkconstants, tkFileDialog
import anonymizer_methods as methods
import os

from Tkinter import *
from ttk import Frame, Style
from shutil import make_archive

class dicom_anonymizer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.dirname=''
        self.dir_opt = {} 
        self.initialize()
        self.field_dict = {}
        
    def initialize(self):
        self.parent.title("DICOM-anonymizer")
        self.style = Style()
        self.style.theme_use("default")
        
        self.parent.minsize(440,100)
        self.grid()
   
        self.entryVariable = Tkinter.StringVar()
        self.entryVariable.set("Select the DICOM directory")

        self.entry = Entry(self, width=40, textvariable=self.entryVariable)
        self.entry.grid(row=1, column=0, padx=15, pady=15)
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

        self.buttonSelect = Button(self, text="Select", command=self.askdirectory)
        self.buttonSelect.grid(row=1, column=1, padx=(0,15), pady=15)

        self.buttonsPanel = Frame(self)
        self.buttonsPanel.grid(row=2, column=0, columnspan=2, pady=10)

        self.buttonView = Button(self.buttonsPanel, text="View DICOM fields", command=self.anonymize)
        self.buttonView.grid(row=0, column=0, padx=(0,10))
        self.buttonView.configure(state=DISABLED)

        self.buttonZip = Button(self.buttonsPanel, text="Zip DICOM folder", command=self.zipDicom)
        self.buttonZip.grid(row=0, column=1, padx=(10,0))
        self.buttonZip.configure(state=DISABLED)

        self.parent.resizable(True,False)
        self.center(self.parent)
    
    def center(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))  
    
    def askdirectory(self):

        """Returns a selected directoryname."""
        self.dirname=tkFileDialog.askdirectory(**self.dir_opt)
        self.entryVariable.set(self.dirname)
        self.buttonView.configure(state=NORMAL)
        self.buttonZip.configure(state=NORMAL)
        return self.dirname
        
    def anonymize(self):
        XML_file = "fields_to_zap.xml"    
        field_dict=methods.Grep_DICOM_fields(XML_file)
        field_dict=methods.Grep_DICOM_values(self.dirname, field_dict)
        fields_keys=list(field_dict.keys())
        self.edited_entries=[Tkinter.StringVar() for i in range(len(fields_keys)+1)]
        if len(field_dict)!=0:
            self.field_edit_win = Tkinter.Toplevel(self)
            self.field_edit_win.title('Fields to Edit')
           # self.field_edit_win.geometry("690x450+120+120")
            self.field_edit_win.grid()
            self.field_edit_win.columnconfigure(0, weight=1)
            self.field_edit_win.columnconfigure(1, weight=1)
            self.field_edit_win.rowconfigure(0, weight=1)
             
            
            # Set column names
            self.field_edit_win.Name_field=Tkinter.Label(self.field_edit_win,text="Dicom Field", relief="ridge", width=30, anchor="w", fg="white",bg="#282828")
            self.field_edit_win.Name_field.grid(column=0,row=0, padx=(5,0), pady=(5,0), sticky=N+S+W+E)
            self.field_edit_win.Name_value=Tkinter.Label(self.field_edit_win,text="Value in Dicom", relief="ridge", width=55, anchor="w", fg="white",bg="#282828")
            self.field_edit_win.Name_value.grid(column=1,row=0, padx=(0,5), pady=(5,0), sticky=N+S+W+E)
            
            # Display description of fields to zap in first column
            self.key_index=1
            field_order = []
            for keys in fields_keys:
                self.field_edit_win.Field_label=Tkinter.Label(self.field_edit_win,text=str(field_dict[keys]['Description'])+':', relief="ridge", width=30, anchor="w", fg="black",bg="#B0B0B0")
                self.field_edit_win.Field_label.grid(column=0,row=self.key_index, padx=(5,0), sticky=N+S+W+E)
                # Enter value to modify
                if not field_dict[keys]['Editable']: #kr#
                    var=Tkinter.StringVar()
                    self.field_edit_win.Field=Tkinter.Entry(self.field_edit_win,textvariable=var,state="disable", width=55)
                    if 'Value' in field_dict[keys]:
                        var.set(field_dict[keys]['Value'])
                else:
                    self.field_edit_win.Field=Tkinter.Entry(self.field_edit_win,textvariable=self.edited_entries[self.key_index], width=55)
                    if 'Value' in field_dict[keys]:
                        self.field_edit_win.Field.insert(self.key_index,field_dict[keys]['Value'])
                    else:
                        self.field_edit_win.Field.insert(self.key_index, "")
                self.field_edit_win.Field.grid(column=1,row=self.key_index, padx=(0,5), sticky=N+S+W+E)
                self.field_edit_win.rowconfigure(self.key_index, weight=1)  
                self.key_index+=1
    
            self.field_dict = field_dict
            
            self.bottomPanel = Frame(self.field_edit_win)
            self.bottomPanel.grid(row=self.key_index, column=0, columnspan=2, pady=10)
            
            self.field_edit_win.button_done = Tkinter.Button(self.bottomPanel,text=u"Anonymize",  command=self.collect_edited_data)
            self.field_edit_win.button_done.grid(column=0,row=0, padx=20)

            self.field_edit_win.buttonClear = Tkinter.Button(self.bottomPanel,text=u"Clear",  command=self.clear, width=8)
            self.field_edit_win.buttonClear.grid(column=1,row=0, padx=20)
     

    def clear(self):
         for items in self.edited_entries:
             items.set("")

    def collect_edited_data(self):
         self.field_edit_win.status_label=Tkinter.Label(self.field_edit_win,text='processing data....', anchor="w",fg="white",bg="blue")
         self.field_edit_win.status_label.grid(column=1, row=self.key_index+1)
         
         new_vals = []
         for entries in self.edited_entries:
             new_vals.append(entries.get())
         # Remove the first item (corresponding to the title row in displayed table
         new_vals.pop(0)

         key_nb=0
         for key in self.field_dict.keys():
             if 'Value' in self.field_dict[key]:
                if self.field_dict[key]['Value'] == new_vals[key_nb]:
                    self.field_dict[key]['Update'] = False
                else:
                    self.field_dict[key]['Update'] = True
                    self.field_dict[key]['Value'] = new_vals[key_nb]
             else:
                 self.field_dict[key]['Update'] = False
             key_nb += 1

         (anonymize_dcm, original_dcm) = methods.Dicom_zapping(self.dirname, self.field_dict)
         self.field_edit_win.destroy()
             

    def zipDicom(self):
         directory = self.entry.get()
         archiveName = directory 
         make_archive(archiveName, 'zip', directory)
          
if __name__ == "__main__":
    root = Tk()
    app = dicom_anonymizer(root)
    root.mainloop()
