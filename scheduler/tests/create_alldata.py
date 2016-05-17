import visit
import candidate
import lib.datamanagement as DataManagement
import lib.utilities as Utilities

#create studysetup
#saving (DataManagement.save_study_data(studydb)) after each visit is really not necessary
#but this mimics the way the application will work
# rank, visitlabel, previousvisit=None, visitwindow = None, visitmargin = None, mandatory = 'Yes, actions = None, uid=None
#
studydb = {}
studyvisit = visit.VisitSetup(1, 'V0', None)
studydb[studyvisit.uid] = studyvisit
Utilities.print_object(studyvisit)
DataManagement.save_study_data(studydb)
studyvisit = visit.VisitSetup(2, 'V1', 'V0', 10, 2)
studydb[studyvisit.uid] = studyvisit
DataManagement.save_study_data(studydb)
studyvisit = visit.VisitSetup(3, 'V2', 'V1', 20, 10)
studydb[studyvisit.uid] = studyvisit
DataManagement.save_study_data(studydb)

#create a list of candidate
#saving (DataManagement.save_candidate_data(candidatedb)) after each candidate is really not necessary
#firstname, lastname, phone, uid=None, visitset = None, status = None, pscid=None, **kwargs
#but this mimics the way the application wil work
candidatedb = {}
candidatedata = candidate.Candidate('Billy', 'Roberts', '451-784-9856', otherphone='514-874-9658')
candidatedb[candidatedata.uid] = candidatedata
DataManagement.save_candidate_data(candidatedb)

candidatedata = candidate.Candidate('Sue', 'Allen', '451-874-9632', None, None, None, 1234567)
candidatedb[candidatedata.uid] = candidatedata
DataManagement.save_candidate_data(candidatedb)

candidatedata = candidate.Candidate('Alan', 'Parson', '451-874-8965')
candidatedb[candidatedata.uid] = candidatedata
DataManagement.save_candidate_data(candidatedb)

candidatedata = candidate.Candidate('Pierre', 'Tremblay', '547-852-9745')
candidatedb[candidatedata.uid] = candidatedata
DataManagement.save_candidate_data(candidatedb)

candidatedata = candidate.Candidate('Alain', 'Jeanson', '245-874-6321')
candidatedb[candidatedata.uid] = candidatedata
DataManagement.save_candidate_data(candidatedb)

candidatedata = candidate.Candidate('Marc', 'St-Pierre', '412-897-9874')
candidatedb[candidatedata.uid] = candidatedata
DataManagement.save_candidate_data(candidatedb)


#add visit data to candidates
db = dict(DataManagement.read_candidate_data())
#get all key values
keylist = []
for key in db:
    keylist.append(key)

candidate1 = db.get(keylist[0])
visitlabel = 'V0'  #TODO selection from droplist
visitdate = '2014-12-25'  #TODO add regex controls
visittime = '13:15' #TODO add regex controls
visitwhere = 'CRIUGM lobby'
visitwhom = 'Annie'
thisvisit = candidate1.set_visit_date(visitlabel, visitdate, visittime, visitwhere, visitwhom)
candidate1.set_next_visit_window(candidate1, thisvisit)
DataManagement.save_candidate_data(db)
Utilities.print_object(thisvisit)

candidate2 = db.get(keylist[1])
visitlabel = 'V0'  #TODO selection from droplist
visitdate = '2014-12-27'  #TODO add regex controls
visittime = '14:30' #TODO add regex controls
visitwhere = 'CRIUGM M-124'
visitwhom = 'Jean'
thisvisit = candidate2.set_visit_date(visitlabel, visitdate, visittime, visitwhere, visitwhom)
candidate2.set_next_visit_window(candidate2, thisvisit)
DataManagement.save_candidate_data(db)

candidate2 = db.get(keylist[1])
visitlabel = 'V1'  #TODO selection from droplist
visitdate = '2015-02-07'  #TODO add regex controls
visittime = '09:15' #TODO add regex controls
visitwhere = 'CRIUGM M-124'
visitwhom = 'Jean'
thisvisit = candidate2.set_visit_date(visitlabel, visitdate, visittime, visitwhere, visitwhom)
candidate2.set_next_visit_window(candidate2, thisvisit)
DataManagement.save_candidate_data(db)

candidate3 = db.get(keylist[2])
visitlabel = 'V0'  #TODO selection from droplist
visitdate = '2015-01-13'  #TODO add regex controls
visittime = '09:15' #TODO add regex controls
visitwhere = 'McDo'
visitwhom = 'Scott'
thisvisit = candidate3.set_visit_date(visitlabel, visitdate, visittime, visitwhere, visitwhom)
candidate3.set_next_visit_window(candidate3, thisvisit)
DataManagement.save_candidate_data(db)

candidate4 = db.get(keylist[3])
visitlabel = 'V0'  #TODO selection from droplist
visitdate = '2015-02-24'  #TODO add regex controls
visittime = '15:30' #TODO add regex controls
visitwhere = 'IGA'
visitwhom = 'Charlie'
thisvisit = candidate4.set_visit_date(visitlabel, visitdate, visittime, visitwhere, visitwhom)
candidate4.set_next_visit_window(candidate4, thisvisit)

DataManagement.save_candidate_data(db)
