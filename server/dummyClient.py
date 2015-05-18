import httplib
import thread
import time
import threading


class MyThread(threading.Thread):
  def __init__(self, id):
    threading.Thread.__init__(self)
    self.id = id

  def run(self):
    print "Start execute thread ", self.id
    self.sendRequest()
    print "End Thread ",self.id

  def sendRequest(self):
    print "ana are mere"
    conn = httplib.HTTPConnection("192.168.1.168:9000")
    conn.request("GET","/putHeartRate?value="+str(self.id)+"&time="+str(time.time()))
    res = conn.getresponse()
    #print "request: ", self.id, " ---- ", res.status, res.reason
    conn.request("GET","/putNumSteps?value="+str(self.id)+"&time="+str(time.time()))
    res = conn.getresponse()
    if self.id == 5 or self.id == 7:
      conn.request("GET","/getChartsData")
      res = conn.getresponse()
    print "request: ", self.id, " ---- ", res.status, res.reason


num = 0
for i in xrange(10):
  num += 1
  t = MyThread(num)
  t.start()
  time.sleep(0.01)



    