import candidate

happycandidate = candidate.Candidate('Billy', 'Roberts', '451-784-9856', otherphone='514-874-9658')


for attr, value in happycandidate.__dict__.iteritems():
    print attr, " = ",  value
