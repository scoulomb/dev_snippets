def unixPythonPathInit():
    import sys
    import os
    DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
    DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
    #print DOSSIER_PARENT
    sys.path.append(DOSSIER_PARENT)

import os
if os.name == 'posix': # linux
    unixPythonPathInit()


from couchbase import Couchbase
from couchbase.exceptions import CouchbaseError

from ValueGen import ValueGen
import uuid
import time
import multiprocessing

class WorkloadGenerator(multiprocessing.Process):

    def __init__(self):
        super(WorkloadGenerator, self).__init__()
        self.bookGen = ValueGen()

    def run(self):
        self.c = Couchbase.connect(bucket='default', host='localhost')
     
        print "Starting workload injector"

        while True :
                   
            doc = self.bookGen.makeValue()
            key = str(uuid.uuid1())
            self.c.set(key, doc)
    
   




if __name__ == '__main__':
    nbofSubprocess = 10

    for i in range(0, nbofSubprocess):
        s = WorkloadGenerator()
        s.start()
        


