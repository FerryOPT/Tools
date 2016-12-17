from CommonWrapper import *

warn_logger = lambda : NotImplementedError

@retry()
def always_fail():
    raise RuntimeError

print 1234

always_fail()