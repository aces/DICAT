#!/usr/bin/python

import Tkinter, tkFileDialog, tkMessageBox
import os
from Tkinter import *

# Internal classes import
import lib.dicom_anonymizer_methods as methods
'''
lib.resource_path_methods has been created for Pyinstaller.
Need to load images or external files using these methods, otherwise the
created application would not find them.
'''
import lib.resource_path_methods as PathMethods


'''
Determine which de-identifier tool to use (PyDICOM or DICOM toolkit) before
starting the program.
Will exit with an error message if neither PyDICOM or DICOM toolkit were found.
'''
deidentifier_tool = methods.find_deidentifier_tool()
if not deidentifier_tool:
    message = "Error: no tool was found to read or de-identify DICOM files."
    tkMessageBox.showinfo("Message", message)
    exit()


class dicom_deidentifier_frame_gui(Frame):
    def __init__(self, parent):
        self.parent = parent
        self.dirname = ''
        self.dir_opt = {}
        self.field_dict = {}
        self.message = StringVar()
        self.initialize()


    def initialize(self):

        # initialize main Frame
        self.frame = Frame(self.parent)
        self.frame.pack(expand=1, fill='both')

        self.frame.columnconfigure(0, weight=6)
        self.frame.columnconfigure(1, weight=1)

        # Initialize default text that will be in self.entry
        self.entryVariable = Tkinter.StringVar()
        self.entryVariable.set("Select a DICOM directory")

        # Create an entry with a default text that will be replaced by the path
        # to the directory once directory selected
        self.entry = Entry(self.frame,
                           width=40,
                           textvariable=self.entryVariable
                          )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

        # Create a select button to use to select a DICOM directory
        self.buttonSelect = Button(self.frame,
                                   text=u"Select",
                                   command=self.askdirectory
                                  )
        self.buttonsPanel = Frame(self.frame)

        self.entry.grid(row=0, column=0, padx=15, pady=10, sticky=E + W)
        self.buttonSelect.grid(row=0,
                               column=1,
                               padx=(0, 15),
                               pady=10,
                               sticky=E + W)
        self.buttonsPanel.grid(row=1, column=0, columnspan=2, pady=(4, 16))

        self.buttonView = Button(self.buttonsPanel,
                                 text=u"View DICOM fields",
                                 command=self.deidentify)
        self.buttonView.grid(row=0, column=0, padx=(0, 10), sticky=E + W)
        self.buttonView.configure(state=DISABLED)

        self.messageView = Label( self.frame,
                                  textvariable=self.message,
                                )
        self.messageView.grid( row=2,
                               column=0,
                               columnspan=2,
                               padx=(0, 10),
                               sticky=E + W
                             )
        self.messageView.grid_forget()

    def askdirectory(self):

        # removes the message from the grid
        self.messageView.grid_forget()

        """Returns a selected directory name."""
        self.dirname = tkFileDialog.askdirectory(**self.dir_opt)
        self.entryVariable.set(self.dirname)
        self.buttonView.configure(state=NORMAL)
        return self.dirname

    def deidentify(self):

        # clear edit table if it exists
        if hasattr(self, 'field_edit_win'):
            self.field_edit_win.destroy()

        # Read the XML file with the identifying DICOM fields
        load_xml = PathMethods.resource_path("data/fields_to_zap.xml")
        XML_filename  = load_xml.return_path()

        # Remove the message from the grid
        self.messageView.grid_forget()

        if os.path.isfile(XML_filename):
            XML_file = XML_filename
        else:
            XML_filepath = os.path.dirname(os.path.abspath(__file__))
            XML_file = XML_filepath + "/" + XML_filename
        field_dict = methods.grep_dicom_fields(XML_file)

        # Read DICOM header and grep identifying DICOM field values
        field_dict = methods.grep_dicom_values(self.dirname, field_dict)

        fields_keys = list(field_dict.keys())
        keys_length = len(fields_keys) + 1
        self.edited_entries = [Tkinter.StringVar() for i in range(keys_length)]
        if len(field_dict) != 0:
            self.field_edit_win = Frame(self.parent)
            self.field_edit_win.pack(expand=1, fill='both')
            self.field_edit_win.columnconfigure(0, weight=1)
            self.field_edit_win.columnconfigure(1, weight=1)
            self.field_edit_win.rowconfigure(0, weight=1)
            self.field_edit_win.rowconfigure(1, weight=1)

            # Set column names
            self.field_edit_win.Name_field = Tkinter.Label(self.field_edit_win,
                                                           text="Dicom Field",
                                                           relief="ridge",
                                                           width=30,
                                                           anchor="w",
                                                           fg="white",
                                                           bg="#282828")
            self.field_edit_win.Name_field.grid(column=0,
                                                row=0,
                                                padx=(5, 0),
                                                pady=(5, 0),
                                                sticky=N + S + W + E)
            self.field_edit_win.Name_value = Tkinter.Label(
                self.field_edit_win,
                text="Value in Dicom",
                relief="ridge",
                width=55,
                anchor="w",
                fg="white",
                bg="#282828")
            self.field_edit_win.Name_value.grid(column=1,
                                                row=0,
                                                padx=(0, 5),
                                                pady=(5, 0),
                                                sticky=N + S + W + E)

            # Display description of fields to zap in first column
            self.key_index = 1
            for keys in fields_keys:
                self.field_edit_win.Field_label = Tkinter.Label(
                    self.field_edit_win,
                    text=str(field_dict[keys]['Description']) + ':',
                    relief="ridge", width=30, anchor="w", fg="black",
                    bg="#B0B0B0")
                self.field_edit_win.Field_label.grid(column=0,
                                                     row=self.key_index,
                                                     padx=(5, 0),
                                                     sticky=N + S + W + E)
                # Enter value to modify
                if not field_dict[keys]['Editable']:  # kr#
                    var = Tkinter.StringVar()
                    self.field_edit_win.Field = Tkinter.Entry(
                        self.field_edit_win, textvariable=var, state="disable",
                        width=55)
                    if 'Value' in field_dict[keys]:
                        var.set(field_dict[keys]['Value'])
                else:
                    self.field_edit_win.Field = Tkinter.Entry(
                        self.field_edit_win,
                        textvariable=self.edited_entries[self.key_index],
                        width=55)
                    if 'Value' in field_dict[keys]:
                        self.field_edit_win.Field.insert(self.key_index,
                                                         field_dict[keys][
                                                             'Value'])
                    else:
                        self.field_edit_win.Field.insert(self.key_index, "")
                self.field_edit_win.Field.grid(column=1, row=self.key_index,
                                               padx=(0, 5),
                                               sticky=N + S + W + E)
                self.field_edit_win.rowconfigure(self.key_index, weight=1)
                self.key_index += 1

            self.field_dict = field_dict

            self.bottomPanel = Tkinter.Frame(self.field_edit_win)
            self.bottomPanel.grid(row=self.key_index, column=0, columnspan=2,
                                  pady=10)

            self.field_edit_win.button_done = Tkinter.Button(
                self.bottomPanel,
                text=u"De-identify",
                command=self.collect_edited_data)
            self.field_edit_win.button_done.grid(column=0, row=0, padx=20)

            self.field_edit_win.buttonClear = Tkinter.Button(self.bottomPanel,
                                                             text=u"Clear",
                                                             command=self.clear,
                                                             width=8)
            self.field_edit_win.buttonClear.grid(column=1, row=0, padx=20)

    def clear(self):
        for items in self.edited_entries:
            items.set("")

    def collect_edited_data(self):

        self.field_edit_win.config(cursor="watch")
        self.field_edit_win.update()
        new_vals = []
        for entries in self.edited_entries:
            new_vals.append(entries.get())
        # Remove the first item (corresponding to the title row in the
        # displayed table)
        new_vals.pop(0)

        key_nb = 0
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

        # Edit DICOM field values to de-identify the dataset
        # (deidentified_dcm, original_dcm) = ''
        (deidentified_dcm, original_dcm) = methods.dicom_zapping(
            self.dirname, self.field_dict)

        self.field_edit_win.destroy()
        if os.path.exists(deidentified_dcm) != [] and os.path.exists(
                original_dcm) != []:
            self.message.set("BOOYA! It's de-identified!")
            self.messageView.configure( fg="dark green",
                                    font= "Helvetica 16 bold italic"
                                  )
            self.messageView.grid( row=2,
                                   column=0,
                                   columnspan=2,
                                   padx=(0, 10),
                                   sticky=E+W
                                 )
        else:
            self.message.set("An error occured during DICOM files de-identification")
            self.messageView.configure( fg="dark red",
                                        font= "Helvetica 16 italic"
                                      )
            self.messageView.grid( row=2,
                                   column=0,
                                   columnspan=2,
                                   padx=(0, 10),
                                   sticky=E+W
                                 )
