import httplib
import thread
import time
import threading
import sys

HOST_NAME = '192.168.1.168' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.

class MyThread(threading.Thread):
  def __init__(self, id):
    threading.Thread.__init__(self)
    self.id = id

  def run(self):
    print "Start execute thread ", self.id
    self.sendRequest()
    print "End Thread ",self.id

  def sendRequest(self):
    conn = httplib.HTTPConnection(HOST_NAME + ":" + str(PORT_NUMBER))
    conn.request("GET","/putHeartRate?value="+str(self.id)+"&time="+str(time.time()))
    res = conn.getresponse()
    #print "request: ", self.id, " ---- ", res.status, res.reason
    conn.request("GET","/putNumSteps?value="+str(self.id)+"&time="+str(time.time()))
    res = conn.getresponse()
    #if self.id == 5 or self.id == 7:
    #  conn.request("GET","/getChartsData")
    #  res = conn.getresponse()
    print "request: ", self.id, " ---- ", res.status, res.reason

if __name__ == '__main__':
  if len(sys.argv) == 2:
    PORT_NUMBER = int(sys.argv[1])
  if len(sys.argv) == 3:
    HOST_NAME = sys.argv[1]
    PORT_NUMBER = int(sys.argv[2])

  num = 0
  for i in xrange(10):
    num += 1
    t = MyThread(num)
    t.start()
    time.sleep(6)



    