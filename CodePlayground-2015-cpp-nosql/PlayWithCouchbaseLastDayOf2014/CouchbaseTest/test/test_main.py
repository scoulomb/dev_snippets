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

    def __init__(self, tps):
        super(WorkloadGenerator, self).__init__()
        self.tps = tps
        self.bookGen = ValueGen()

    def run(self):
        self.c = Couchbase.connect(bucket='default', host='localhost')
     
        print "Starting workload injector"

        while True :
            start_t = time.time()
            for _ in range(self.tps):
                            
                doc = self.bookGen.makeValue()
                #print doc
                #doc = "sylvain"
                key = str(uuid.uuid1())
                self.c.set(key, doc)
    
            if (time.time() - start_t) > 1:
                print "WARNING ! Client is not able to reach the # of TPS required ..."
            else:
                time.sleep(1 - (time.time() -start_t))





if __name__ == '__main__':

    tps = 10000
    nbofSubprocess = tps/30

    for i in range(0, nbofSubprocess):
        s = WorkloadGenerator(30)
        s.start()
        


