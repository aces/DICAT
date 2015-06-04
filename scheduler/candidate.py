import datetime
import visit
import lib.datamanagement as datamanagement
import lib.multilanguage as multilanguage
import lib.utilities as utilities
from uuid import uuid1

class Candidate():
    def __init__(self, firstname, lastname, phone, uid=None, visitset = None, status = None, pscid=None, **kwargs): #TODO *kwarg
        self.uid = utilities.generateUniqueID()
        self.firstname = firstname
        self.lastname = lastname
        self.visitset = visitset
        self.phone = phone
        self.status = status
        self.pscid = pscid
        #...many other attributes
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                setattr(self, key, value)
    
            
    def setupvisitset(self):
        #open studysetup.db and 'parse' the dict to a sorted list (dict cannot be sorted)...
        visitlist =[]
        visitlabel_templist = []
        try: 
            studysetup = dict(datamanagement.readstudydata())  #TODO replace datafile name
        except Exception as e:
            print str(e)  #TODO add error login  
        for key, value in studysetup.iteritems():
            visitlist.append(studysetup[key])     
        visitlist = sorted(visitlist, key=lambda visit: visit.rank)
        #...and create a temporary list of visitlabels that will serve a key within the Candidate.visitset dictionary
        for each in visitlist:
            visitlabel_templist.append(each.visitlabel) #we now have a list with all visit labels included in the study     
        #instantiate individual visit based on each instance of StudySetup()
        self.visitset = {}  #setup a dict to receive a set of Visit()
        count = 0
        #set values of :  uid, rank, visitlabel, previousvisit, visitwindow, visitmargin,
        for key in visitlist:
            mainkey = str(visitlabel_templist[count])
            rank =key.rank
            visitlabel = key.visitlabel
            previousvisit = key.previousvisit
            visitwindow = key.visitwindow
            visitmargin = key.visitmargin
            visitdata = visit.Visit(rank, visitlabel, previousvisit, visitwindow, visitmargin,)
            self.visitset[mainkey] = visitdata
            count += 1
        self.status = multilanguage.status_active
    
        
    def setvisitdate(self, visitlabel, visitdate, visittime, visitwhere, visitwhom):
        #check to see if visitset == None before trying to create a new date instance
        if self.visitset is None:
            self.setupvisitset()
        #get current visit within visitset
        current = self.visitset.get(visitlabel)
        #check to see if this visit already has a date
        if current.when is not None:
            print "date already exists"  #TODO add confirmation of change  log???
            pass
        #concatenate visitdate and visittime and parse into a datetime object
        visitwhen = visitdate + ' ' + visittime
        when = datetime.datetime.strptime(visitwhen, '%Y-%m-%d %H:%M')
        #set 'current' values of :  when, where, withwhom, status
        current.when = when
        current.where = visitwhere
        current.withwhom = visitwhom
        current.status = "active"
        return current

                         
    def setnextvisitwindow(self, candidate,  currentvisit):
        #get the current visit object as argument.  Will search and look for the next visit (visit where previousvisit == currentvisitlabel)
        nextvisitsearchset = candidate.visitset
        currentvisitlabel = currentvisit.visitlabel
        nextvisit = ""
        for key in nextvisitsearchset:
            visitdata = nextvisitsearchset[key]
            if visitdata.previousvisit == currentvisitlabel:
                nextvisit = candidate.visitset.get(visitdata.visitlabel) #TODO debug when current is last visit
        #gather info about currentvisit (mostly for my own internal computer!)        
        currentvisitdate = currentvisit.when
        currentvisityear = currentvisitdate.year #get the year of the current visit date
        nextvisitwindow = nextvisit.visitwindow
        nextvisitmargin = nextvisit.visitmargin
        #set dates for the next visit
        nextvisitearly = int(currentvisitdate.strftime('%j')) + (nextvisitwindow - nextvisitmargin) #this properly handle change of year
        nextvisitearlydate = datetime.datetime(currentvisityear, 1, 1) + datetime.timedelta(nextvisitearly - 1)
        nextvisitlate = int(currentvisitdate.strftime('%j')) + (nextvisitwindow + nextvisitmargin)
        nextvisitlatedate = datetime.datetime(currentvisityear, 1, 1) + datetime.timedelta(nextvisitlate - 1)
        nextvisit.whenearliest = nextvisitearlydate
        nextvisit.whenlatest = nextvisitlatedate
        nextvisit.status = "tentative"


    def getactivevisit(self, candidate):
        candidatefullname = str(candidate.firstname + ' ' + candidate.lastname)
        currentvisitset = candidate.visitset
        if currentvisitset is None:
            return
        elif currentvisitset is not None:
            for key in currentvisitset:
                if currentvisitset[key].status == multilanguage.status_active:
                    visitlabel = currentvisitset[key].visitlabel
                    when = currentvisitset[key].when.strftime('%Y-%m-%d %Hh%m')
                    where = currentvisitset[key].where
                    who = currentvisitset[key].withwhom
                    activevisit = [candidatefullname, visitlabel, when, where, who]
        return activevisit
  
