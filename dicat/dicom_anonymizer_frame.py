#!/usr/bin/python

import Tkinter, tkFileDialog, tkMessageBox, ttk
import os
import re
from Tkinter import *

# Internal classes import
import lib.dicom_anonymizer_methods as methods
'''
lib.resource_path_methods has been created for Pyinstaller.
Need to load images or external files using these methods, otherwise the
created application would not find them.
'''
import lib.resource_path_methods as PathMethods



class dicom_deidentifier_frame_gui(Frame):
    def __init__(self, parent):
        self.parent = parent
        self.dirname = ''
        self.dir_opt = {}
        self.field_dict = {}
        self.message = StringVar()

        # Determine if PyDICOM python library is present.
        deidentifier_tool = methods.find_deidentifier_tool()
        if not deidentifier_tool:
            error = "ERROR: PyDICOM does not appear to be installed.\n "      \
                    + "Please make sure PyDICOM has been properly installed " \
                    + "before using the DICOM deidentifier tab.\n "           \
                    + "Check the README.md of the DICAT repository for "     \
                    + "information on how to install PyDICOM."
            self.message.set(error)

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
        self.entry = Entry(
            self.frame, width=40, textvariable=self.entryVariable
        )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

        # Create a select button to use to select a DICOM directory
        self.buttonSelect = Button(
            self.frame, text=u"Select", command=self.askdirectory
        )
        self.buttonsPanel = Frame(self.frame)

        self.entry.grid(row=0, column=0, padx=15, pady=10, sticky=E + W)
        self.buttonSelect.grid(
            row=0, column=1, padx=(0, 15), pady=10, sticky=E + W
        )
        self.buttonsPanel.grid(row=1, column=0, columnspan=2, pady=(4, 16))

        self.buttonView = Button(
            self.buttonsPanel, text=u"View DICOM fields", command=self.deidentify
        )
        self.buttonView.grid(row=0, column=0, padx=(0, 10), sticky=E + W)
        self.buttonView.configure(state=DISABLED)

        self.messageView = Label(self.frame, textvariable=self.message)
        self.messageView.grid(
            row=2, column=0, columnspan=2, padx=(0, 10), sticky=E + W
        )
        if self.message.get():
            # if error message is set due to not finding the tool, show the error on the screen
            self.messageView.configure(
                fg="dark red", font="Helvetica 16 bold italic"
            )
        else:
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
            self.topPanel.destroy()

        # Remove the message from the grid
        self.messageView.grid_forget()

        # load XML file and create the field dictionary
        XML_file   = methods.load_xml("data/fields_to_zap.xml")
        field_dict = methods.grep_dicom_fields(XML_file)

        # Read DICOM header and grep identifying DICOM field values
        field_dict = methods.grep_dicom_values(self.dirname, field_dict)

        if not field_dict:
            message = "No valid DICOM file was found in " + self.dirname
            tkMessageBox.showinfo("Error", message)

        # print out a warning message at the top of the table
        self.topPanel = Tkinter.Frame(self.parent)
        self.topPanel.pack(fill='both', expand=1)

        info_bold_msg = "WARNING: Every value present in the 'Value in DICOM file'" \
                        "column will be written in the DICOM headers.\n"
        info_body_msg = "To erase all header values from the DICOMs: " \
                        "  1) click on 'Clear All Fields' " \
                        "  2) enter the new PatientName for the study " \
                        "  3) click on 'De-identify'"

        self.info_msg = Text(self.topPanel, padx=40, wrap='word', height=3)
        self.info_msg.tag_configure('bold',    font=('Verdana', 12, 'bold'), foreground='red2')
        self.info_msg.tag_configure('default', font=('Verdana', 12),         foreground='red2')
        self.info_msg.insert(END, info_bold_msg, 'bold')
        self.info_msg.insert(END, info_body_msg, 'default')

        self.scrollTopPanel = Scrollbar(self.topPanel, command=self.info_msg.yview)
        self.info_msg.configure(yscrollcommand=self.scrollTopPanel.set)

        self.info_msg.pack(fill='both', side="left", expand=1)
        self.scrollTopPanel.pack(fill='y', side='right')
        self.info_msg.config(state='disabled')


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

            # set column names
            self.keep_all = 0
            self.field_edit_win.Name_field = Tkinter.Label(
                self.field_edit_win, text="DICOM field name", relief="sunken",
                width=30,            anchor="w",              fg="white",
                bg="#282828",        height=2
            )
            self.field_edit_win.Name_value = Tkinter.Label(
                self.field_edit_win, text="Value in DICOM file", relief="sunken",
                width=55,            anchor="w",                 fg="white",
                bg="#282828",        height=2
            )

            # display the column names on the grid
            self.field_edit_win.Name_field.grid(
                column=0, row=0, padx=(5, 0), sticky='nsew'
            )
            self.field_edit_win.Name_value.grid(
                column=1, row=0, padx=(0, 0), sticky='nsew'
            )

            # Display description of fields to zap in first column
            self.key_index = 1
            for keys in fields_keys:

                # set the Editable of the dictionary to True for all entries now
                # that they are all editable in the GUI. Note, the reason we don't
                # modify the XML here is so that the mass_deidentifier can still
                # run with only PatientName, DoB and Gender as editable
                field_dict[keys]['Editable'] = True

                # set DICOM field names and DICOM values
                label_text  = str(field_dict[keys]['Description']) + ":"
                pname_color = "black"
                if label_text == 'PatientName:':
                    label_text += ' (IDs to label the scan are required)'
                    pname_color = "#006400"
                self.field_edit_win.Field_label = Tkinter.Label(
                    self.field_edit_win, text=label_text, relief='ridge',
                    width=30,            anchor="w",      fg=pname_color,
                    bg='#C0C0C0'
                )
                self.field_edit_win.Field = Tkinter.Entry(
                    self.field_edit_win,
                    textvariable=self.edited_entries[self.key_index],
                    width=55,
                )
                if pname_color == "#006400":
                    self.field_edit_win.Field.configure(
                        highlightbackground=pname_color
                    )

                # display the values found in the DICOM file into the Entry field
                if 'Value' in field_dict[keys]:
                    self.edited_entries[self.key_index].set(
                        field_dict[keys]['Value']
                    )
                else:
                    self.edited_entries[self.key_index].set("")

                # display table content
                self.field_edit_win.Field_label.grid(
                    column=0, row=self.key_index, padx=(5, 0), sticky='nsew'
                )
                self.field_edit_win.Field.grid(
                    column=1, row=self.key_index, padx=(0, 0), sticky='nsew'
                )
                self.field_edit_win.rowconfigure(self.key_index, weight=1)
                self.key_index += 1

            self.field_dict = field_dict

            self.bottomPanel = Tkinter.Frame(self.field_edit_win)
            self.bottomPanel.grid(
                row=self.key_index, column=0, columnspan=3, pady=10
            )

            self.field_edit_win.button_done = Tkinter.Button(
                self.bottomPanel,
                text=u"De-identify",
                command=self.collect_edited_data
            )
            self.field_edit_win.button_done.grid(column=1, row=0, padx=20)

            self.field_edit_win.buttonClear = Tkinter.Button(
                self.bottomPanel, text=u"Clear All Fields", command=self.clear
            )
            self.field_edit_win.buttonClear.grid(column=2, row=0, padx=20)

    def clear(self):
        for items in self.edited_entries:
            items.set("")

    def collect_edited_data(self):

        self.field_edit_win.config(cursor="watch")
        self.field_edit_win.update()
        new_vals = []
        for entries in self.edited_entries:
            new_vals.append(entries.get())
        # Remove the first item (corresponding to the title row in the displayed table)
        new_vals.pop(0)

        key_nb = 0
        pname_set = 0
        for key in self.field_dict.keys():
            if re.match(r'PatientName', str(self.field_dict[key]['Description'])):
                if new_vals[key_nb]:
                    pname_set = 1
            methods.update_DICOM_value(self.field_dict, key, new_vals[key_nb])
            key_nb += 1

        if not pname_set:
            tkMessageBox.showinfo("ERROR", "PatientName DICOM field is required to label the scan")
            self.deidentify()
        else:
            # Edit DICOM field values to de-identify the dataset (deidentified_dcm, original_dcm) = ''
            (deidentified_dcm, original_dcm) = methods.dicom_zapping(self.dirname, self.field_dict)

            self.field_edit_win.destroy()
            self.topPanel.destroy()
            if os.path.exists(deidentified_dcm) != [] and os.path.exists(original_dcm) != []:
                self.message.set("BOOYA! It's de-identified!")
                self.messageView.configure(fg="dark green", font= "Helvetica 16 bold italic")
                self.messageView.grid(row=2, column=0, columnspan=2, padx=(0, 10), sticky=E+W)
            else:
                self.message.set("An error occured during DICOM files de-identification")
                self.messageView.configure(fg="dark red", font="Helvetica 16 italic")
                self.messageView.grid(row=2, column=0, columnspan=2, padx=(0, 10), sticky=E + W)
