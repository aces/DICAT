#!/usr/bin/env python_32
# -*- coding: iso-8859-1 -*-

try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

from xml.dom import minidom

class simpleapp_wx(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.IDMap = {}
        self.sizer = wx.GridBagSizer()

        self.candidatename = wx.TextCtrl(self,-1,value=u"Real name")
        self.candidateid = wx.TextCtrl(self, -1, value=u"Identifier")
        self.sizer.Add(self.candidatename, (0,0),(1,1), wx.EXPAND)
        self.sizer.Add(self.candidateid, (0,1),(1,1), wx.EXPAND)
        #sizer.Add(self.candidateid,(1,1),(2,2),wx.EXPAND)
        #self.Bind(wx.EVT_TEXT_ENTER, self.OnPressEnter, self.candidatename)

        button = wx.Button(self,-1,label="Add candidate")
        self.sizer.Add(button, (0,2), (1, 1), wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.AddIdentifierEvent, button)

        #button = wx.Button(self, -1, label="Save map")
        #self.Bind(wx.EVT_BUTTON, self.SaveMapEvent, button)
        #self.sizer.Add(button, (1, 2))


        self.datatable = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.datatable.InsertColumn(0, "Identifier")
        self.datatable.InsertColumn(1, "Real Name")
        self.sizer.Add(self.datatable, (2, 0), (1, 2), wx.EXPAND)

        self.LoadXML("candidates.xml")

            
        self.sizer.AddGrowableCol(0)
        self.SetSizerAndFit(self.sizer)
        #self.SetSizeHints(-1,self.GetSize().y,-1,self.GetSize().y );
        #self.candidatename.SetFocus()
        #self.candidatename.SetSelection(-1,-1)
        self.Show(True)

    def LoadXML(self, file):
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
        f = open("candidates.xml", "w")
        f.write("<?xml version=\"1.0\"?>\n<data>\n")
        print self.IDMap
        for key in self.IDMap:
            f.write("\t<Candidate>\n")
            f.write("\t\t<Identifier>%s</Identifier>\n" % key)
            f.write("\t\t<RealName>%s</RealName>\n" % self.IDMap[key])
            f.write("\t</Candidate>\n")
        f.write("</data>")

    def SaveMapEvent(self, event):
        self.SaveMapAction()



    def AddIdentifierEvent(self,event):
        name = self.candidatename.GetValue()
        id = self.candidateid.GetValue()
        self.AddIdentifierAction(id, name)

    def AddIdentifierAction(self, candid, realname, save=True):
        self.IDMap[candid] = realname

        idx = self.datatable.InsertStringItem(0, candid)
        self.datatable.SetStringItem(idx, 1, realname)

        if(save):
            self.SaveMapAction()
        self.sizer.Fit(self)

if __name__ == "__main__":
    app = wx.App()
    frame = simpleapp_wx(None,-1,'my application')
    app.MainLoop()
