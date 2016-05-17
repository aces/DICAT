import lib as utilities
import lib as datamanagement

db = dict(datamanagement.read_candidate_data())

utilities.printobject(db)
