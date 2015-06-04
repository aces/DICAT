import visit
import candidate
import lib.datamanagement as datamanagement

#create studysetup
studydb = {}
studyvisit = visit.StudySetup(1, 'V0')
studydb[studyvisit.uid] = studyvisit
studyvisit = visit.StudySetup(2, 'V1', 'V0', 10, 2)
studydb[studyvisit.uid] = studyvisit
studyvisit = visit.StudySetup(3, 'V2', 'V1', 20, 10)
studydb[studyvisit.uid] = studyvisit
datamanagement.savestudydata(studydb)

#create a list of candidate
candidatedb = {}
candidatedata = candidate.Candidate('Billy', 'Roberts', '451-784-9856', otherphone='514-874-9658')
candidatedb[candidatedata.uid] = candidatedata
candidatedata = candidate.Candidate('Sue', 'Allen', '451-874-9632')
candidatedb[candidatedata.uid] = candidatedata
candidatedata = candidate.Candidate('Alan', 'Parson', '451-874-8965')
candidatedb[candidatedata.uid] = candidatedata
candidatedata = candidate.Candidate('Pierre', 'Tremblay', '547-852-9745')
candidatedb[candidatedata.uid] = candidatedata
candidatedata = candidate.Candidate('Alain', 'Jeanson', '245-874-6321')
candidatedb[candidatedata.uid] = candidatedata
candidatedata = candidate.Candidate('Marc', 'St-Pierre', '412-897-9874')
candidatedb[candidatedata.uid] = candidatedata
datamanagement.savecandidatedata(candidatedb)

#add visit data to candidates
db = dict(datamanagement.readcandidatedata())
#get all key values
keylist = []
for key in db:
    keylist.append(key)

candidate1 = db.get(keylist[0])
candidate2 = db.get(keylist[1])
candidate3 = db.get(keylist[2])
candidate4 = db.get(keylist[3])
candidate5 = db.get(keylist[4])

visitlabel = 'V0'  #TODO selection from droplist
visitdate = '2014-12-25'  #TODO add regex controls
visittime = '13:15' #TODO add regex controls
visitwhere = 'CRIUGM lobby'
visitwhom = 'Annie'
thisvisit = candidate1.setvisitdate(visitlabel, visitdate, visittime, visitwhere, visitwhom)
candidate1.setnextvisitwindow(candidate1, thisvisit)

visitlabel = 'V1'  #TODO selection from droplist
visitdate = '2014-12-27'  #TODO add regex controls
visittime = '14:30' #TODO add regex controls
visitwhere = 'CRIUGM M-124'
visitwhom = 'Jean'
thisvisit = candidate2.setvisitdate(visitlabel, visitdate, visittime, visitwhere, visitwhom)
candidate2.setnextvisitwindow(candidate2, thisvisit)

visitlabel = 'V1'  #TODO selection from droplist
visitdate = '2015-01-13'  #TODO add regex controls
visittime = '09:15' #TODO add regex controls
visitwhere = 'McDo'
visitwhom = 'Scott'
thisvisit = candidate3.setvisitdate(visitlabel, visitdate, visittime, visitwhere, visitwhom)
candidate3.setnextvisitwindow(candidate3, thisvisit)

visitlabel = 'V0'  #TODO selection from droplist
visitdate = '2015-02-24'  #TODO add regex controls
visittime = '15:30' #TODO add regex controls
visitwhere = 'IGA'
visitwhom = 'Charlie'
thisvisit = candidate4.setvisitdate(visitlabel, visitdate, visittime, visitwhere, visitwhom)
candidate4.setnextvisitwindow(candidate4, thisvisit)

datamanagement.savecandidatedata(db)
