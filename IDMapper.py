#!/usr/bin/env python_32
# -*- coding: iso-8859-1 -*-

try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

from xml.dom import minidom

class TunahackIDMapper(wx.Frame):
    def __init__(self,parent,id,title):
        """Initialize the application"""
        wx.Frame.__init__(self,parent,id,title)
        self.parent = parent

        # Initialize all the wxPython components
        self.InitUI()

        # Set up the dictionary map
        self.IDMap = {}

        # Load the data
        self.LoadXML("candidates.xml")

        # Show the window only after loading data
        # This is specific to wxPython, but can't go into
        # InitUI because first we need to load the data
        self.Show(True)

    def InitUI(self):
        """Sets up all wxPython related UI elements"""
        self.sizer = wx.GridBagSizer()

        # Add the textboxes for data entry
        self.candidatename = wx.TextCtrl(self,-1,value=u"")
        self.candidateid = wx.TextCtrl(self, -1, value=u"")

        self.sizer.Add(self.candidatename, (1,1),(1,1), wx.EXPAND)
        self.sizer.Add(self.candidateid, (1,0),(1,1), wx.EXPAND)

        label = wx.StaticText(self, label="Identifier")
        self.sizer.Add(label, (0, 0), (1, 1), wx.EXPAND)

        label = wx.StaticText(self, label="Real Name")
        self.sizer.Add(label, (0, 1), (1, 1), wx.EXPAND)
        # Add the Add Candidate button
        button = wx.Button(self,-1,label="Add candidate")
        self.sizer.Add(button, (1,2), (1, 1), wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.AddIdentifierEvent, button)

        self.ErrorMessage = wx.StaticText(self, label="")
        self.sizer.Add(self.ErrorMessage, (2, 2), (1, 1), wx.EXPAND)


        # Create the data table
        self.datatable = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.datatable.InsertColumn(0, "Identifier")
        self.datatable.InsertColumn(1, "Real Name")
        self.sizer.Add(self.datatable, (2, 0), (1, 2), wx.EXPAND)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick, self.datatable)
        # Some final cleanup for GridBagSizer
        self.sizer.AddGrowableCol(0)
        self.SetSizerAndFit(self.sizer)

    def LoadXML(self, file):
        """Parses the XML file and loads the data into the current window"""
        try:
            xmldoc = minidom.parse(file)
            itemlist = xmldoc.getElementsByTagName('Candidate')
            for s in itemlist:
                identifier = s.getElementsByTagName("Identifier")[0].firstChild.nodeValue
                realname = s.getElementsByTagName("RealName")[0].firstChild.nodeValue

                self.AddIdentifierAction(identifier, realname, False)
        except:
            pass

    def SaveMapAction(self):
        """Function which performs the action of writing the XML file"""
        f = open("candidates.xml", "w")
        f.write("<?xml version=\"1.0\"?>\n<data>\n")
        for key in self.IDMap:
            f.write("\t<Candidate>\n")
            f.write("\t\t<Identifier>%s</Identifier>\n" % key)
            f.write("\t\t<RealName>%s</RealName>\n" % self.IDMap[key])
            f.write("\t</Candidate>\n")
        f.write("</data>")

    def SaveMapEvent(self, event):
        """Handles any wxPython event which should trigger a save action"""
        self.SaveMapAction()

    def AddIdentifierEvent(self,event):
        """
        Handles any wxPython event which should trigger adding an identifier to the
        data table and gets the appropriate values to be added to the mapping
        """
        name = self.candidatename.GetValue()
        id = self.candidateid.GetValue()
        self.AddIdentifierAction(id, name)

    def AddIdentifierAction(self, candid, realname, save=True):
        """
        Adds the given identifier and real name to the mapping. If
        the "save" parameter is true, this also triggers the saving
        of the XML file. 
        This is set to False on initial load.
        """

        self.ErrorMessage.SetLabel("")
        if candid in self.IDMap:
            self.ErrorMessage.SetLabel("ERROR: Candidate\nkey already exists")
            self.sizer.Fit(self)
            return

        self.IDMap[candid] = realname

        idx = self.datatable.InsertStringItem(0, candid)
        self.datatable.SetStringItem(idx, 1, realname)

        if(save):
            self.SaveMapAction()
        self.sizer.Fit(self)

    def OnClick(self, event):
        pass
        #import pdb; pdb.set_trace()
        #name = self.candidatename.SetValue("abc")
        #id = self.candidateid.SetValue("def")

if __name__ == "__main__":
    app = wx.App()
    frame = TunahackIDMapper(None,-1,'Hack-a-Tuna ID Mapper')
    app.MainLoop()
