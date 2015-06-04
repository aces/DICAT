#!/usr/bin/env python 

#Python Tkinter imports
from Tkinter import *
from ttk import *

#local imports
import lib.multilanguage as multilanguage
import lib.datamanagement as datamanagement
import newwindow


class ApplicationGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title(multilanguage.apptitle)  #TODO modify
        self.pack(side=TOP, expand=YES, fill=BOTH, padx=10, pady=10)
        
        self.create_menubar()
        self.projectinfopane =Labelframe(self, text=multilanguage.project_infopane, width=250, height=350, borderwidth=10) #TODO add dynamic resize
        self.projectinfopane.pack(side=LEFT, expand=NO, fill=BOTH)
        #datapane is composed of one PanedWindow containing two Labelframe
        self.datapane = Panedwindow(self, width = 1000, height = 500, orient=HORIZONTAL)   #TODO add dynamic resize
        self.datapane.pack(side=RIGHT, expand=YES, fill=BOTH)
        #self.projectinfopane =Labelframe(self.datapane, text='Project Information', width=100, height=350, borderwidth=10) #TODO add dynamic resize  #TODO clean
        self.candidatepane = Labelframe(self.datapane, text=multilanguage.candidate_pane, width=100, height=350, borderwidth=10) #TODO add dynamic resize
        self.visitpane = Labelframe(self.datapane, text=multilanguage.calendar_pane, width=100, height=350, borderwidth=10) #TODO add dynamic resize
        #self.datapane.add(self.projectinfopane)  #TODO clean
        
        self.datapane.add(self.candidatepane)
        self.datapane.add(self.visitpane)
        
        #get data from *.db files
        data = dict(datamanagement.readcandidatedata())#TODO place data management elsewhere
        #create data tables (treeview)
        visitcolheaders = ('candidate', 'visitlabel', 'when', 'where', 'status')
        self.visittable = DataTable(self.visitpane, data, visitcolheaders)
        self.visittable.pack(side=BOTTOM, expand=YES, fill=BOTH)  
        colheaders = ('firstname', 'lastname', 'phone', 'status')
        datatable = DataTable(self.candidatepane, data, colheaders)
        datatable.pack(side=BOTTOM, expand=YES, fill=BOTH)

        

    def create_menubar(self): #TODO try to replace by class
        #create toplevel menubar
        self.menubar = Menu(self)
        #create an APPLICATION pulldown menu
        self.applicationmenu = Menu(self.menubar, tearoff = 0)
        self.applicationmenu.add_command(label = multilanguage.settingapplication, command=self.appsettings)
        self.applicationmenu.add_separator()
        self.applicationmenu.add_command(label = multilanguage.quitapplication, command=self.quitapplication)
        #create a CANDIDATE pulldown menu
        self.candidatemenu = Menu(self.menubar, tearoff = 0)
        self.candidatemenu.add_command(label = multilanguage.addcandidate, command = self.addcandidate)
        self.candidatemenu.add_command(label = multilanguage.findcandidate, command = self.findcandidate)
        self.candidatemenu.add_command(label = multilanguage.updatecandidate, command = self.updatecandidate)
        self.candidatemenu.add_separator()
        self.candidatemenu.add_command(label = multilanguage.getcandidateid, command = self.getcandidateid)
        self.candidatemenu.add_separator()
        self.candidatemenu.add_command(label= multilanguage.excludecandidate, command = self.excludecandidate)
        #create a CALENDAR pulldown menu
        self.calendarmenu = Menu(self.menubar, tearoff = 0)
        self.calendarmenu.add_command(label = multilanguage.newappointment, command=self.opencalendar)
        #create a DICOM_anonymizer pulldown men
        self.anonymizermenu = Menu(self.menubar, tearoff = 0)  #TODO add relevant menu
        self.anonymizermenu.add_command(label = "menu")
        #create a HELP pulldown menu
        self.helpmenu = Menu(self.menubar, tearoff = 0)
        self.helpmenu.add_command(label = multilanguage.gethelp, command=self.openhelp)
        self.helpmenu.add_command(label = multilanguage.aboutwindow, command=self.aboutapplication)
        #add all menu to the menubar        
        self.menubar.add_cascade(label = multilanguage.menuapplication, menu = self.applicationmenu)
        self.menubar.add_cascade(label = multilanguage.menucandidate, menu = self.candidatemenu)
        self.menubar.add_cascade(label = multilanguage.menucalendar, menu = self.calendarmenu)
        self.menubar.add_cascade(label = multilanguage.menuanonymizer, menu = self.anonymizermenu)
        #self.menubar.add_cascade(label = multilanguage.menuhelp, menu = self.helpmenu) #TODO add help menu
        #add the menubar to the parent frame
        self.parent.config(menu = self.menubar)


    def appsettings(self):
        print 'running appsettings'
        pass
    
    def quitapplication(self):
        print 'running quitapplication'
        self.quit()
        pass
    
    def opencalendar(self):
        print 'running opencalendar'
        pass
    
    def addcandidate(self):
        print 'running addcandidate'
        pass
    
    def findcandidate(self):
        print 'running findcandidate'
        pass
    
    def updatecandidate(self):
        print 'running updatecandidate'
        pass
    
    def getcandidateid(self):
        print 'running getcandidateid'
        pass
    
    def excludecandidate(self):
        print 'running incativatecandidate'
        pass
    
    def openhelp(self):
        print 'running openhelp'
        pass
    
    def aboutapplication(self):
        print 'running aboutapplication'
        pass
    
    

        
#############################################################################################################################
class DataTable(Frame):
    def __init__(self, parent, dataset, colheaders): #expected is dataset
        Frame.__init__(self)
        self.parent = parent
        colheaders = colheaders
        dataset = dataset
        datatable = self.initdatatable(parent, colheaders)
        self.updatedata(datatable,dataset, colheaders)
     
    def initdatatable(self, parent, colheaders):   
        self.datatable = Treeview(parent, selectmode='browse', columns=colheaders, show="headings")
        for col in colheaders:
            self.datatable.heading(col, text=col.title(), command=lambda c=col: self.treeview_sortby(self.datatable, c, 0))
            self.datatable.column(col, width=100, stretch="Yes", anchor="center")        
        self.verticalscroll = Scrollbar(parent, orient="vertical", command=self.datatable.yview)
        self.horizontalscroll = Scrollbar(parent, orient="horizontal", command=self.datatable.xview)
        self.datatable.configure(yscrollcommand=self.verticalscroll.set, xscroll=self.horizontalscroll.set)
        self.verticalscroll.pack(side=RIGHT, expand=NO, fill=BOTH)
        self.horizontalscroll.pack(side=BOTTOM, expand=NO, fill=BOTH)
        self.datatable.pack(side=LEFT, expand=YES, fill=BOTH) 


    def treeview_sortby(self, tree, column, descending):
        """Taken from Dave's IDmapper"""
        """Sort tree contents when a column is clicked on."""
        """From: https://code.google.com/p/python-ttk/source/browse/trunk/pyttk-samples/treeview_multicolumn.py?r=21"""
        # grab values to sort
        data = [(tree.set(child, column), child) for child in tree.get_children('')]
        # reorder data
        data.sort(reverse=descending)
        for index, item in enumerate(data):
            tree.move(item[1], '', index)
            # switch the heading so that it will sort in the opposite direction
            tree.heading(column, command=lambda column=column: self.treeview_sortby(tree, column, int(not descending)))
        

    #TODO move to dataManagement      
    def updatedata(self, datatable, dataset, colheaders):
        if 'firstname' in colheaders:
            # This method will add cantidates information to cantidatetable
            try:
                for key in dataset:
                    if dataset[key].status is None:
                        status = ''
                    else:
                        status = dataset[key].status
                    self.datatable.insert('', 'end', values=[dataset[key].firstname, dataset[key].lastname, dataset[key].phone, status], tags=(status, dataset[key].uid, 'candidate'))
            except Exception as e:
                print "Exception AddIdentifierAction(self, dataset, save=True): " + str(e)
                #utilities.errorlog(message)
                pass #TODO add some error handling
            self.datatable.tag_configure('active', background='#ccffcc')  #TODO set color in application settings and preferences
            self.datatable.bind('<Double-1>', self.ondoubleclick)
            
        elif 'candidate' in colheaders:
            currentvisitset = {}
            for key, value in dataset.iteritems():
                if dataset[key].visitset is not None: #skip the search if visitset = None
                    currentvisitset = dataset[key].visitset  #set this candidate.visitset for the next step
                    #gather information about the candidate
                    candidatekey = dataset[key].uid  #not printed on screen but saved with the new Scheduler object (after all it is the candidate unique id^^)
                    candidatefirstname = dataset[key].firstname
                    candidatelastname = dataset[key].lastname
                    candidatefullname = str(candidatefirstname + ' ' + candidatelastname)
                    for key, value in currentvisitset.iteritems():
                        if currentvisitset[key].status is not None:
                            visitlabel = currentvisitset[key].visitlabel
                            if currentvisitset[key].when is None:
                                when = currentvisitset[key].whenearliest
                            else:
                                when = currentvisitset[key].when
                            if currentvisitset[key].where is None:
                                where = ''
                            else:
                                where = currentvisitset[key].where
                            #whom = currentvisitset[key].withwhom
                            if currentvisitset[key].status is None:
                                status = ''
                            else:
                                status = currentvisitset[key].status
                            #print candidatefullname, visitlabel, when, where, whom  #TODO remove
                            #TODO ? create a new scheduler object with these informations
                            
                            # This method will add planned visits information to the visit datatable
                            try:
                                self.datatable.insert('', 'end', values= [candidatefullname, visitlabel, when, where, status], tags=(status, candidatekey, 'schedule', visitlabel))
                            except Exception as e:
                                print "Exception AddIdentifierAction(self, dataset, save=True): " + str(e)  #TODO remove
                                #utilities.errorlog(message)
                                pass #TODO add some error handling
            self.datatable.tag_configure('active', background='#ccffcc')   #TODO set in application settings and preferences
            self.datatable.tag_configure('tentative', background='#f0f0f1')   #TODO set in application settings and preferences
            self.datatable.bind('<Double-1>', self.ondoubleclick)
            
    def ondoubleclick(self, event):
        # double clicking on blank space of the treeview will generate an IndexOutOfRange error
        try:
            item_id = self.datatable.selection()[0]
            item = self.datatable.item(item_id)['tags']
            candidate = item[1]
            function = item[2]
            if function == "schedule":
                visitlabel = item[3]
            else:
                visitlabel = None
        except Exception as e:
            print str(e) #TODO error management
            return
        parent = self.parent
        if function == "schedule":
            newwin = newwindow.NewWindow(parent, candidate, function, visitlabel)
        elif function == "candidate":
            newwin = newwindow.NewWindow(parent, candidate, function, visitlabel)
        else:
            return
        
            
#############################################################################################################################

#self-test "module"  TODO remove 
if __name__ == '__main__':
    root = Tk()
    
    #root.geometry() #TODO add dynamic resize
    app = ApplicationGUI(root)
    
    root.protocol("WM_DELETE_WINDOW", app.quitapplication)
    app.mainloop()
    
