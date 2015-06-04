"""
a045a534-a31f-11e4-bc02-fc4dd4d3c3f3
a04493c0-a31f-11e4-9414-fc4dd4d3c3f3
a045a533-a31f-11e4-aba9-fc4dd4d3c3f3
a045a532-a31f-11e4-96a6-fc4dd4d3c3f3
a045a531-a31f-11e4-a1c4-fc4dd4d3c3f3
"""

import visit
import candidate
import lib.datamanagement as datamanagement
import lib.utilities as utilities

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


"""
#########################################################################
#########################################################################

print '\nGUI:  print on screen all active visits (sorted by datetime)' 
currentvisitset = {}
for key, value in candidatedb.iteritems():
    if candidatedb[key].visitset is not None: #skip the search if visitset = None
        currentvisitset = candidatedb[key].visitset  #set this candidate.visitset for the next step
        #gather information about the candidate
        candidatekey = candidatedb[key].uid  #not printed on screen but saved with the new Scheduler object (after all it is the candidate unique id^^)
        candidatefirstname = candidatedb[key].firstname
        candidatelastname = candidatedb[key].lastname
        for key, value in currentvisitset.iteritems():
            if currentvisitset[key].status is not None:
                visitlabel = currentvisitset[key].visitlabel
                when = currentvisitset[key].when
                where = currentvisitset[key].where
                whom = currentvisitset[key].withwhom
                status = currentvisitset[key].status
                print candidatefirstname, candidatelastname, visitlabel, when, where, whom, status
                #create a new scheduler object with these informations


    
"""
