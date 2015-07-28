import candidate
import visit
import datetime
import lib.datamanagement as datamanagement

#loading data
candidatedb = dict(datamanagement.read_candidate_data())
#GUI:  selecting a candidate from db
#print '\nGUI:  SELECTING ONE CANDIDATE,...'
happycandidate = candidatedb.get("a045a530-a31f-11e4-9c66-fc4dd4d3c3f3")
#Upon setting the first visit with a candidate, we will dump a complete visitset into candidate.visitset
#set values of :  visitlabel, visitdate, visittime, where, whom
#print '\nGUI:   ...AND SETTING UP THE FIRST VISIT (date, time...)'
#print 'system:  collecting information from application'
visitlabel = 'V0'  #TODO selection from droplist
visitdate = '2014-12-22'  #TODO add regex controls
visittime = '13:15' #TODO add regex controls
visitwhere = 'CRIUGM lobby'
visitwhom = 'me'
#print 'system:  create visitset instance if necessary and add collected information to proper visit in Candidate.visitset'
thisvisit = happycandidate.set_visit_date(visitlabel, visitdate, visittime, visitwhere, visitwhom)
happycandidate.set_next_visit_window(happycandidate, thisvisit)
#print'\nGUI:  NOW THIS CANDIDATE HAS A DATE FOR HIS/HER FIRST VISIT + A RANGE FOR THE FOLLOWING VISIT'
#print '\nGUI:  put on screen all active visits (sorted by datetime)  =>  see test3.py'
datamanagement.save_candidate_data(candidatedb)


#TESTED
