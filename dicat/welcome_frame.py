#!/usr/bin/python

# import from standard packages
from Tkinter import *
import tkFileDialog

# import from DICAT libraries
import lib.config as Config
import lib.resource_path_methods as PathMethods # needed for PyInstaller builds

class welcome_frame_gui(Frame):
    """
    Welcome frame GUI class.

    """

    def __init__(self, parent):
        """
        Initialization of the welcome frame gui class.

        :param parent: parent widget in which to display the welcome frame
         :type parent: object

        """

        self.parent = parent
        self.description_frame_gui()
        self.load_database_gui()


    def description_frame_gui(self):
        """
        Draws the description frame with the LOGO image.

        """

        frame = Frame(self.parent)
        frame.pack(expand=1, fill='both')


        # Insert DICAT logo on the right side of the screen
        load_img = PathMethods.resource_path("images/DICAT_logo.gif")
        imgPath  = load_img.return_path()
        logo     = PhotoImage(file = imgPath)
        logo_image = Label(frame,
                           image = logo,
                           bg='white'
                          )
        logo_image.image = logo

        logo_image.pack(side='left', fill='both')

        # Create the Welcome to DICAT text variable
        text   = Text(frame, padx=40, wrap='word')
        scroll = Scrollbar(frame, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.tag_configure('title',
                           font=('Verdana', 20, 'bold', 'italic'),
                           justify='center'
                          )
        text.tag_configure('bold',    font=('Verdana', 12, 'bold'))
        text.tag_configure('default', font=('Verdana', 12))

        # Insert title into the text variable
        title = "\nWelcome to DICAT!\n\n"
        text.insert(END, title, 'title')

        # Insert introduction of the tool into the text variable
        intro  = "DICAT (DICOM Anonymization Tool) is a simple tool for "
        intro += "de-identification of DICOM datasets. In addition to "
        intro += "de-identifying DICOM files, this tool contains a feature "
        intro += "that allows mapping the candidate's information to its "
        intro += "study identifier.\n"
        text.insert(END, intro, 'default')

        # Insert explanation of the DICOM anonymizer tab into the text variable
        tab1 = "\n\nThe DICOM de-identifier tab allows to:\n"
        text.insert(END, tab1, 'bold')

        anonymizer  = '''
        1) select a DICOM directory
        2) view the DICOM headers information
        3) run the de-identifier tool on all DICOMs of the selected directory
        '''
        text.insert(END, anonymizer, 'default')

        # Insert explanation of the ID key tab into the text variable
        tab2 = "\n\nThe ID key tab allows to:\n"
        text.insert(END, tab2, 'bold')

        IDkey = '''
        1) store ID information for a given candidate
        2) look for ID information from a given candidate
        '''
        text.insert(END, IDkey, 'default')

        # Insert explanation of the scheduler tab into the text variable
        tab3 = "\n\nThe scheduler tab allows to:\n"
        text.insert(END, tab3, 'bold')

        # TODO: develop on the functionality of scheduler
        Sched = '''
        1) Store patient information
        2) Schedule visits
        3) View the schedule
        4) blablabla
        '''
        text.insert(END, Sched, 'default')


        # Display the text variable
        text.pack(side='left', fill='both', expand=1)
        scroll.pack(side="right", fill='y')
        # Disable the edit functionality of the displayed text
        text.config(state='disabled')


    def load_database_gui(self):
        """
        Load database GUI including:
            - a button to create a new database based on a template file
            - a button to select and open an existing database
            - an entry where the path to the loaded database file is displayed

        """

        frame = Frame(self.parent, bd=5, relief='groove')
        frame.pack(expand=0, fill='both')

        # Label
        label = Label(
            frame,
            text=u"Open a DICAT database (.xml file)",
            font=('Verdana', 15, 'bold', 'italic')
        )

        # select an existing candidate.xml file
        # Initialize default text that will be in self.entry
        self.entryVariable = StringVar()
        self.entryVariable.set("Open a DICAT database (.xml file)")

        # Create an entry with a default text that will be replaced by the path
        # to the XML file once directory selected
        entry = Entry(
            frame, width=60, textvariable=self.entryVariable
        )
        entry.focus_set()
        entry.selection_range(0, END)

        # Create an open button to use to select an XML file with candidate's
        # key info
        buttonOpen = Button(
            frame,
            text=u"Open an existing database",
            command=self.open_existing_database
        )

        buttonCreate = Button(
            frame,
            text=u"Create a new database",
            command=self.create_new_database
        )

        label.grid(
            row=0, column=0, columnspan=3, padx=(0,15), pady=0, sticky=E+W
        )
        buttonCreate.grid(
            row=1, column=0, padx=(15,15), pady=10, sticky=E+W
        )
        buttonOpen.grid(
            row=1, column=1, padx=(0,15), pady=10, sticky=E+W
        )
        entry.grid(
            row=1, column=2, padx=(0,15), pady=10, sticky=E+W
        )


    def open_existing_database(self):
        """
        Opens and loads the selected XML database in DICAT.

        """

        self.filename = tkFileDialog.askopenfilename(
            filetypes=[("XML files", "*.xml")]
        )
        self.entryVariable.set(self.filename)

        if self.filename:
            # Set the database xmlfile in Config.xmlfile to self.filename
            Config.xmlfile = self.filename
        else:
            #TODO: proper error handling
            print "file could not be opened."

        print Config.xmlfile


    def create_new_database(self):
        """
        Uses a template XML file to create a new database and saves it.

        """

        self.filename = tkFileDialog.asksaveasfilename(
            defaultextension=[("*.xml")],
            filetypes=[("XML files", "*.xml")]
        )
        self.entryVariable.set(self.filename)

        # Fetch the database template file
        load_template = PathMethods.resource_path("data/database_template.xml")
        template_file = load_template.return_path()

        # If both the new file and the template file exists, copy the template
        # lines in the new file
        if self.filename and template_file:
            # Set the database xmlfile in Config.xmlfile to self.filename
            Config.xmlfile = self.filename
            with open(Config.xmlfile, 'a') as f1:
                for line in open(template_file, 'r'):
                    f1.write(line)
