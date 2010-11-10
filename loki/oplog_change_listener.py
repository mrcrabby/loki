import sys
import time
from pymongo import Connection

class OpLog(object):
    def __init__(self, mongo_conn, interested_collection):
        self.conn = mongo_conn
	self.coll = interested_collection
	db = conn['local']
	coll = db['oplog.rs']
	self.cur = coll.find({"ns" : interested_collection}, tailable=True)
	self.opmap = {"n" : "beginning", "i" : "insert", "d" : "delete", "u" : "update"}
    def readnext(self):
        doc = self.cur.next() 
	operation = self.opmap[doc['op']]
	if operation == "update":
	    doc_id = doc["o2"]["_id"]
	elif operation == "insert" or operation == "delete":
	    doc_id = doc["o"]["_id"]
	return {"op" : operation, "id" : doc_id}


class ConsoleNotifier(object):
    def write(self,doc):
        print doc

class OplogChangeWatcher(object):
    def __init__(self, oplog, notifier):
	self.oplog = oplog
	self.notifier = notifier
    def run(self):
        while(True):
	    try:
                try:
	            doc = self.oplog.readnext()
		    notifier.write(doc)
		except StopIteration:
		    time.sleep(5)
	    except KeyboardInterrupt:
	        sys.exit(0)


if __name__ == '__main__':
    conn = Connection()
    log = OpLog(conn, "test.foo")
    notifier = ConsoleNotifier()
    watcher = OplogChangeWatcher(log, notifier)
    watcher.run()
