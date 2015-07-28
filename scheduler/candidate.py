#import standard packages
import datetime
import visit
#import internal packages
import lib.datamanagement as DataManagement
import lib.multilanguage as MultiLanguage
import lib.utilities as Utilities

class Candidate():
    """
    The Candidate() class defines the candidates/participants of the study

    Attributes:
        uid:        A unique identifier using python's uuid1 method. Used as key to store and retrieve objects from
                    files and/or dictionaries.
        firstname:  First name of the candidate
        lastname:   Last name of the candidate
        visitset:   A dictionnary containing all visits (planed or not)
        phone:      A primary phone number
        status:     Status of this candidate
        pscid:      Loris (clinical results database) specific ID

        kwargs:     Not implemented yet!

    Code example:
        candidatedb = {} #setup a dict to receive the candidates
        candidatedata = candidate.Candidate('Billy', 'Roberts', '451-784-9856', otherphone='514-874-9658') #instanciate one candidate
        candidatedb[candidatedata.uid] = candidatedata  #add candidate to dict
        DataManagement.save_candidate_data(candidatedb) #save data to file
    """
    def __init__(self, firstname, lastname, phone, uid=None, visitset = None, status = None, pscid=None, **kwargs): #TODO *kwarg
        self.uid = Utilities.generate_uid()
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

    def setup_visitset(self):
        """
        When creating the first visit for a candidate, a complete set of visits is added based on a study/project visit list
        There are no parameters passed to this method since it will simply create a new 'empty'
        This method will:
            1-open studydata (the study visit list) and 'parse' the dict to a sorted list (dict cannot be sorted)
            2-create a temporary list of visit_labels that will serve as a key within the Candidate.visit_set dictionary
            3-instantiate individual visits based on the study visit list
        Usage:
            Called by Candidate.set_visit_date()
        """
        visit_list =[]
        visit_label_templist = []
        study_setup = dict()
        try:
            #1-open studydata
            study_setup = dict(DataManagement.read_studydata())
        except Exception as e:
            print str(e)  #TODO add error login (in case a study data file does not exist)
        for key, value in study_setup.iteritems():
            #2-parse into a sorted list
            visit_list.append(study_setup[key])
        visit_list = sorted(visit_list, key=lambda visit: visit.rank)
        #create a temporary list of visitlabels
        for each in visit_list:
            visit_label_templist.append(each.visitlabel)
        #3-instantiate individual visit based on each instance of VisitSetup()
        self.visitset = {}  #setup a dict to receive a set of Visit()
        count = 0
        #set values of :  uid, rank, visit_label, previous_visit, visit_window, visitmargin,
        for key in visit_list:
            mainkey = str(visit_label_templist[count])
            rank =key.rank
            visit_label = key.visitlabel
            previous_visit = key.previousvisit
            visit_window = key.visitwindow
            visit_margin = key.visitmargin
            visit_data = visit.Visit(rank, visit_label, previous_visit, visit_window, visit_margin,)
            self.visitset[mainkey] = visit_data
            count += 1
        
    def set_visit_date(self, visitlabel, visitdate, visittime, visitwhere, visitwhom):
        """
        This method update the visit information (according to visitlabel)
        This method will:
            1-Check if visitset==None. If so, then Candidate.setup_visitset() is called to setup Candidate.visitset
            2-Check if a date is already set for this visitlabel
            3-Set values of Visit.when, 'Visit.where, Visit.whithwhom and Visit.status for current visit
        Usage: Called by GUI methods
        Return: current_visit as current Visit(Visit(VisitSetup) instance
        """
        #1-Check to see if visitset == None before trying to create a new date instance
        if self.visitset is None:
            self.setup_visitset()
            self.set_candidate_status_active() #Candidate.status='active' since we're setting up a first visit
        #get current visit within visitset
        current_visit = self.visitset.get(visitlabel)
        #2-Check to see if this visit already has a date
        if current_visit.when is not None:
            print "date already exists"  #TODO add confirmation of change log???
            pass
        #concatenate visitdate and visittime and parse into a datetime object
        visitwhen = visitdate + ' ' + visittime
        when = datetime.datetime.strptime(visitwhen, '%Y-%m-%d %H:%M')
        #3-Set values of Visit.when, 'Visit.where, Visit.whithwhom and Visit.status for current visit
        current_visit.when = when
        current_visit.where = visitwhere
        current_visit.withwhom = visitwhom
        current_visit.status = "active"  #that is the status of the visit
        return current_visit


    """
    def set_next_visit_window(self, candidate, current_visit):
        #get the current visit object as argument.  Will search and look for the next visit (visit where previousvisit == current_visit_label)
        next_visit_searchset = candidate.visitset
        current_visit_label = current_visit.visitlabel
        next_visit = ""
        for key in next_visit_searchset:
            visit_data = next_visit_searchset[key]
            if visit_data.previousvisit == current_visit_label:
                next_visit = candidate.visitset.get(visit_data.visitlabel) #TODO debug when current is last visit
        #gather info about current_visit (mostly for my own biological computer! else I get lost)
        current_visit_date = current_visit.when
        current_visit_year = current_visit_date.year #get the year of the current visit date
        next_visit_window = next_visit.visitwindow
        next_visit_margin = next_visit.visitmargin
        #set dates for the next visit
        next_visit_early = int(current_visit_date.strftime('%j')) + (next_visit_window - next_visit_margin) #this properly handle change of year
        next_visit_early_date = datetime.datetime(current_visit_year, 1, 1) + datetime.timedelta(next_visit_early - 1)
        next_visit_late = int(current_visit_date.strftime('%j')) + (next_visit_window + next_visit_margin)
        next_visit_late_date = datetime.datetime(current_visit_year, 1, 1) + datetime.timedelta(next_visit_late - 1)
        next_visit.when_earliest = next_visit_early_date
        next_visit.when_latest = next_visit_late_date
        next_visit.status = "tentative"
        Utilities.print_object((next_visit))
    """
    def set_next_visit_window(self, candidate,  current_visit):
        """
        This method will 'calculate' a min and max date when the next visit should occur
        1-Get candidate.visitset (as visit_searchset) and current_visit.visitlabel
        2-Identify which visit (in visitset) has previousvisit == current_visit.visitlabel
        3-Get
        Usage:  Currently called by GUI function (TODO RETHINK THIS LOGIC maybe it should be called when running Candidate.set_visit_date())
        """


        #get the current visit object as argument.  Will search and look for the next visit (visit where previousvisit == current_visitlabel)

        #1- Get Candidate.visitset and current_visit /  next_visit will == Visit(VisitSetup) of the next visit (relative to current_visit)
        visit_searchset = candidate.visitset
        current_visitlabel = current_visit.visitlabel
        next_visit = ""
        #2-Identify which visit (in visitset) has previousvisit == current_visit.visitlabel
        for key in visit_searchset:
            visit_data = visit_searchset[key]
            if visit_data.previousvisit == current_visitlabel:
                next_visit = candidate.visitset.get(visit_data.visitlabel) #TODO debug when current is last visit
        #3-Calculate a min and max date for the next visit to occur based on Visit.visitwindow and Visit.visitmargin
        current_visitdate = current_visit.when
        current_visityear = current_visitdate.year #get the year of the current visit date
        next_visitwindow = next_visit.visitwindow
        nextvisitmargin = next_visit.visitmargin
        #set dates for the next visit
        nextvisitearly = int(current_visitdate.strftime('%j')) + (next_visitwindow - nextvisitmargin) #this properly handle change of year
        nextvisitearlydate = datetime.datetime(current_visityear, 1, 1) + datetime.timedelta(nextvisitearly - 1)
        nextvisitlate = int(current_visitdate.strftime('%j')) + (next_visitwindow + nextvisitmargin)
        nextvisitlatedate = datetime.datetime(current_visityear, 1, 1) + datetime.timedelta(nextvisitlate - 1)
        next_visit.whenearliest = nextvisitearlydate
        next_visit.whenlatest = nextvisitlatedate
        next_visit.status = "tentative" #set this visit.status

    def get_active_visit(self, candidate):
        candidatefullname = str(candidate.firstname + ' ' + candidate.lastname)
        currentvisitset = candidate.visitset
        activevisit = []
        if currentvisitset is None:
            return
        elif currentvisitset is not None:
            for key in currentvisitset:
                if currentvisitset[key].status == MultiLanguage.status_active:
                    visitlabel = currentvisitset[key].visitlabel
                    when = currentvisitset[key].when.strftime('%Y-%m-%d %Hh%m')
                    where = currentvisitset[key].where
                    who = currentvisitset[key].withwhom
                    activevisit = [candidatefullname, visitlabel, when, where, who]
        return activevisit

    def set_candidate_status_active(self):
        self.status = MultiLanguage.status_active #set the Candidate.status to 'active'