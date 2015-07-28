#import standard packages
#import internal packages
import lib.utilities as utilities
import datetime

class VisitSetup():
    """
    The VisitSetup() class is used to define a study (or project) in terms of sequence of visits and also serves as a
    base class for Visit(VisitSetup).  A study (or project) can have as many visits as required. There is no class for
    study as it is merely a simple dictionnary.

    Code example:  This study contains 3 visits.  Since V0 is the first visit, it doesn't have any values for
                   'previousvisit', 'visitwindow' and ' visitmargin'
                        study = {}
                        visit = visit.VisitSetup(1, 'V0')  #a uid (uuid1) is automatically generated
                        study[visit.uid] = visit           #VisitSetup.uid is a unique ID used as key
                        visit = visit.VisitSetup(2, 'V1', 'V0', 10, 2)
                        study[visit.uid] = visit
                        visit = visit.VisitSetup(3, 'V2', 'V1', 20, 10)
                        study[visit.uid] = visit

    This is the parent class of Visit(VisitSetup), furthermore Visit(VisitSetup) objects will be 'instanciated' from
    each instance of VisitSetup(object).
    Both VisitSetup(object) class and instances are used to create individual instances of Visit(VisitSetup)

    Attributes:
        uid:           A unique identifier using python's uuid1 method. Used as key to store and retrieve objects from
                       files and/or dictionaries.
        rank:          The rank of the visit in the sequence (int). Useful to sort the visits in order of occurrence.
        visitlabel:    The label of the visit (string) such as V1, V2 or anything else the user may come up with
        previousvisit: The visitlabel (string) of the visit occurring before this one. Used to plan this visit based on
                       the date of the previous visit. (default to None)
        visitwindow:   The number of days (int) between this visit and the previous visit.  (default to None)
        visitmargin:   The margin (in number of days (int)) that is an allowed deviation (a +/- few days ).  Basically,
                       this allow the 'calculation' of a date window when this visit should occur.  (default to None)
        mandatory:     Indicate if this visit is mandatory. Default to Yes
        actions:       A list of action points (or simply reminders) specific to that visit (i.e.'reserve room 101').
                       This is not implemented yet (default to None)
    """

    def __init__(self, rank, visitlabel, previousvisit = None, visitwindow = None, visitmargin = None, actions = None, uid=None):
        self.uid = utilities.generate_uid()
        self.rank = rank
        self.visitlabel = visitlabel
        self.previousvisit = previousvisit
        self.visitwindow = visitwindow
        self.visitmargin = visitmargin
        self.actions = actions  #not implemented yet!


class Visit(VisitSetup):
    """
    The Visit(VisitSetup) class help define individual visit of the candidate using VisitSetup(object) instances as 'templates'.
    Upon creation of the first meeting with a candidate, the Candidate(object) instance will get a full set of Visit(VisitSetup) instances.
    This set of visits is contained in Candidate.visitset
    Each time a visit is being setup, a 'time window' is calculated to define the earliest and latest date at which
    the 'nextVisit' should occur.

    Attributes: (In addition of parent class attributes.)
        when:          Date at which this visit is occurring. (default to None)
        when_earliest: Earliest date when this visit should occur. Set to value when previous visit is activated.  (default to None)
        when_latest:   Latest date when this visit should occur. Set to value when previous visit is activated. (default to None)
        where:         Place where this meeting is taking place. (default to None)
        whitwhom:      Professional meeting the study candidate at the reception. (default to None)
        status:        Status of this visit. Set to active when 'when' is set (default to None)
    """
    def __init__(self, rank, visitlabel, previousvisit, visitwindow, visitmargin, actions=None, uid=None, when = None,
                 whenearliest = None, whenlatest = None, where = None, withwhom = None, status = None):
        VisitSetup.__init__(self, rank, visitlabel, previousvisit, visitwindow, visitmargin, actions, uid)
        self.when = when
        self.whenearliest = whenearliest
        self.whenlatest = whenlatest
        self.where = where
        self.withwhom = withwhom
        self.status = status

    def visit_date_range(self):
        print 'I get here'
        early_date = datetime.datetime.date(self.whenearliest)
        late_date = datetime.datetime.date(self.whenlatest)
        date_range = str(early_date), '<>', str(late_date)
        return date_range



