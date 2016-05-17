import lib.utilities as utilities
import lib.datamanagement as datamanagement

db = dict(datamanagement.read_candidate_data())

utilities.printobject(db)
