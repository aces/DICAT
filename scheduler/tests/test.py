import lib.utilities as utilities
import lib.datamanagement as datamanagement

db = dict(datamanagement.readcandidatedata())

utilities.printobject(db)
