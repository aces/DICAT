#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter, Tkconstants, tkFileDialog
import anonymizer_methods as methods

class dicom_anonymizer(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.dirname=''
        self.dir_opt = {} 
        self.initialize()
        self.field_dict = {}
        
        #Tkinter.Button(self, text='askdirectory', command=self.askdirectory).pack(**button_opt)
    def initialize(self):
        self.minsize(100,100)
        self.geometry("551x51")
        self.grid()
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=1,sticky='EW')
        self.entryVariable.set(u"Select the DICOM directory")

        self.button_select = Tkinter.Button(self,text=u"Select",  command=self.askdirectory)
        self.button_select.grid(column=1,row=1)

        self.button_function = Tkinter.Button(self,text=u"View DICOM Fields",  command=self.anonymize)

        
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def askdirectory(self):

        """Returns a selected directoryname."""
        self.dirname=tkFileDialog.askdirectory(**self.dir_opt)
        self.entryVariable.set(self.dirname)
        self.button_function.grid(column=0,row=2)
        return self.dirname
        
    def anonymize(self):
        XML_file = "fields_to_zap.xml"    
        field_dict=methods.Grep_DICOM_fields(XML_file)
        field_dict=methods.Grep_DICOM_values(self.dirname, field_dict)
        fields_keys=list(field_dict.keys())
        self.edited_entries=[Tkinter.StringVar() for i in range(len(fields_keys)+1)]
        if len(field_dict)!=0:
            field_edit_win = Tkinter.Toplevel(self)
            field_edit_win.title('Fields to Edit')
            field_edit_win.geometry("690x450+120+120")
            field_edit_win.grid()
            
            # Set column names
            field_edit_win.Name_field=Tkinter.Label(field_edit_win,text="Dicom Field", relief="ridge", width=30, anchor="w", fg="white",bg="#282828")
            field_edit_win.Name_field.grid(column=1,row=0)
            field_edit_win.Name_value=Tkinter.Label(field_edit_win,text="Value in Dicom", relief="ridge", width=55, anchor="w", fg="white",bg="#282828")
            field_edit_win.Name_value.grid(column=2,row=0)
            
            # Display description of fields to zap in first column
            key_index=1
            field_order = []
            for keys in fields_keys:
                field_edit_win.Field_label=Tkinter.Label(field_edit_win,text=str(field_dict[keys]['Description'])+':', relief="ridge", width=30, anchor="w", fg="black",bg="#B0B0B0")
                field_edit_win.Field_label.grid(column=1,row=key_index, sticky="w")
                # Enter value to modify
                if not field_dict[keys]['Editable']: #kr#
                    var=Tkinter.StringVar()
                    field_edit_win.Field=Tkinter.Entry(field_edit_win,textvariable=var,state="disable", width=55)
                    if 'Value' in field_dict[keys]:
                        var.set(field_dict[keys]['Value'])
                else:
                    field_edit_win.Field=Tkinter.Entry(field_edit_win,textvariable=self.edited_entries[key_index], width=55)
                    if 'Value' in field_dict[keys]:
                        field_edit_win.Field.insert(key_index,field_dict[keys]['Value'])
                    else:
                        field_edit_win.Field.insert(key_index, "")
                field_edit_win.Field.grid(column=2,row=key_index)
                key_index+=1

                   
            self.field_dict = field_dict
            field_edit_win.button_done = Tkinter.Button(field_edit_win,text=u"Anonymize",  command=self.collect_edited_data)
            field_edit_win.button_done.grid(column=1,row=key_index)
     
    def collect_edited_data(self):
         
         new_vals = []
         for entries in self.edited_entries:
             new_vals.append(entries.get())
         # Remove the first item (corresponding to the title row in displayed table
         new_vals.pop(0)

         key_index=0
         for key in self.field_dict.keys():
             if 'Value' in self.field_dict[key]:
                if self.field_dict[key]['Value'] == new_vals[key_index]:
                    self.field_dict[key]['Update'] = False
                else:
                    self.field_dict[key]['Update'] = True
                    self.field_dict[key]['Value'] = new_vals[key_index]
             else:
                 self.field_dict[key]['Update'] = False
             key_index += 1

         (anonymize_dcm, original_dcm) = methods.Dicom_zapping(self.dirname, self.field_dict)
         updated_dict = methods.Grep_DICOM_values(anonymize_dcm, self.field_dict)

          
         
if __name__ == "__main__":
    app = dicom_anonymizer(None)
    app.title('DICOM anonymizer')
    app.mainloop()
