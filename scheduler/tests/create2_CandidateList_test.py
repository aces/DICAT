import candidate
import lib.datamanagement as datamanagement


#GUI:  Setting up a list of candidate
#print '\nGUI:  ENTERING DATA FOR MULTIPLE CANDIDATES'
#TODO add duplicate control by checking for name+phone number
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

datamanagement.save_candidate_data(candidatedb)

#TESTED
