import visit
import lib.datamanagement as datamanagement

#GUI: Setting up the sequence of visit - must be done prior to anything else  
#setup the VisitSetup instances to match the study visit sequence
#the visitdata of each instance will serve to populate individual Visit() instances
#TODO visitlabels MUST start with a letter - ADD regex
#TODO visitlabels MUST be unique

studydb = {}
studyvisit = visit.VisitSetup(1, 'V0')
studydb[studyvisit.uid] = studyvisit

studyvisit = visit.VisitSetup(2, 'V1', 'V0', 10, 2)
studydb[studyvisit.uid] = studyvisit

studyvisit = visit.VisitSetup(3, 'V2', 'V1', 20, 10)
studydb[studyvisit.uid] = studyvisit


datamanagement.save_study_data(studydb)

#TESTED
