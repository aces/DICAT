import lib.utilities as utilities

class StudySetup():
    """
    The StudySetup(object) class define a study in terms of sequence of visits.  
    A study can have as many visits as required and each visit (instance) has its own 'definition'.
    
    This is the parent class of Visit(StudySetup), furthermore the Visit(StudySetup) objects will be 'instanciated' from  each instance of StudySetup(object).
    Both StudySetup(object) class and instances are used to create individual instances of Visit(StudySetup)
    
    uid: unique identifier. Used to store and retrieve object in shelve()
    rank:  The rank of the visit in the sequence (int). Useful to sort the visits in order of occurrence.
    visitlabel:  The label of the visit (string) such as V1, V2 or anything else the user may come up with
    previousvisit: The visitlabel (string) of the visit occurring before this one. Used to plan this visit based on the date of the previous visit. (default to None)
    visitwindow:  The number of days (int) between this visit and the previous visit.  (default to None)
    visitmargin: The margin (in number of days (int)) that is an allowed deviation.  Basically, this allow the 'calculation' of a date window when this visit should occur.  (default to None)
    actions:  A list of action points (or simply reminders) for specific to that visit (i.e.'reserve room 101').  (default to None)
    """
    
    def __init__(self, rank, visitlabel, previousvisit = None, visitwindow = None, visitmargin = None, actions = None, uid=None):
        self.uid = utilities.generateUniqueID()
        self.rank = rank
        self.visitlabel = visitlabel
        self.previousvisit = previousvisit
        self.visitwindow = visitwindow
        self.visitmargin = visitmargin
        self.actions = actions  #not implemented yet!  

        


class Visit(StudySetup):
    """
    The Visit(StudySetup) class help define individual visit of the candidate using StudySetup(object) instances as 'templates'.
    Upon creation of the first meeting with a candidate, the Candidate(object) instance will get a full set of Visit(StudySetup) instances.
    Each time a visit is being setup, a 'time window' is calculated to define the earliest and latest date at which the 'nextVisit' should occur.
    
    In addition of parent class attributes.
    uid: Not used.
    when:  Date at which this visit is occurring. (default to None)
    whenearliest: Earliest date when this visit should occur. Set to value when previous visit is activated.  (default to None)
    whenlatest:  Latest date when this visit should occur. Set to value when previous visit is activated. (default to None)
    where: Place where this meeting is taking place. (default to None)
    whitwhom: Professional meeting the study candidate at the reception. (default to None)
    status:  Status of this visit. Set to active when 'when' is set (default to None)
    """
    def __init__(self, rank, visitlabel, previousvisit, visitwindow, visitmargin, actions=None, uid=None, when = None, whenearliest = None, whenlatest = None, where = None, withwhom = None, status = None):
        StudySetup.__init__(self, rank, visitlabel, previousvisit, visitwindow, visitmargin, actions, uid)
        self.when = when
        self.whenearliest = whenearliest
        self.whenlatest = whenlatest
        self.where = where
        self.withwhom = withwhom
        self.status = status
        

    #def setvisitdate(self, visitdate, visittime, where, whom):
    #    #parse the strings 'visitdate' and 'visittime' to a datetime object before assigning it to Visit instance
    #    #TODO add invalid data/format check
    #    visitdatetimestr = visitdate, ' ', visittime
    #    visitdatetime = datetime.datetime.strptime(visitdatetimestr,"%Y-%m-%d %H:%m") #parse the string to a datetime object
    #    self.when = visitdatetime
    #    self.status = 'active'


    

    

    
    
    
    

        
