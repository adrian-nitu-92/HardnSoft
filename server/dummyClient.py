import httplib
import thread
import time
import threading
import sys


HOST_NAME = '192.168.1.168' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.
ROOT = ""

class MyThread(threading.Thread):
  def __init__(self, id, nrSteps, distance):
    threading.Thread.__init__(self)
    self.id = id
    self.nrSteps = nrSteps
    self.distance = distance

  def run(self):
    print "Start execute thread ", self.id
    self.sendRequest()
    print "End Thread ",self.id

  def sendRequest(self):
    conn = httplib.HTTPConnection(ROOT)
    #conn.request("GET","/putHeartRate?value="+str(self.id)+"&time="+str(time.time())+"&statie=x")
    #res = conn.getresponse()
    #print "request: ", self.id, " ---- ", res.status, res.reason
    conn.request("GET","/putNumSteps?value="+str(self.nrSteps)+"&time="+str(time.time())+"&statie=x")
    res = conn.getresponse()
    print "request: ", self.id, " ---- ", res.status, res.reason
    #from random import randint
    #conn.request("GET","/putAirTemperature?value="+str(randint(2,9))+"&time="+str(time.time())+"&statie=x")
    #res = conn.getresponse()
    #print "request: ", self.id, " ---- ", res.status, res.reason
    #conn.request("GET","/putHumidity?value="+str(randint(-100,100))+"&time="+str(time.time())+"&statie=x")
    #res = conn.getresponse()
    #print "request: ", self.id, " ---- ", res.status, res.reason
    #conn.request("GET","/putAirTemperature?value="+str(randint(-100,100))+"&time="+str(time.time())+"&statie=x")
    #res = conn.getresponse()
    #print "request: ", self.id, " ---- ", res.status, res.reason
    conn.request("GET","/putDistance?value="+str(self.distance)+"&time="+str(time.time())+"&statie=x")
    res = conn.getresponse()
    print "request: ", self.id, " ---- ", res.status, res.reason
    #conn.request("GET","/putTreasure?time="+str(time.time())+"&checkpoint="+str(randint(0,10))+"&value="+str(randint(-100,100))+"&name=dummy")
    #res = conn.getresponse()
    #if self.id == 5 or self.id == 7:
    #  conn.request("GET","/getChartsData")
    #  res = conn.getresponse()
    print "request: ", self.id, " ---- ", res.status, res.reason

if __name__ == '__main__':
  print len(sys.argv)
  ROOT = sys.argv[1]

#  ROOT = socket.gethostbyname(HOST_NAME)
#  ROOT = ROOT
# + ":" + str(PORT_NUMBER)
  print ROOT
  distance = 0
  while True:
    for i in xrange(10):
      distance = distance + 1
      t = MyThread(i+1, distance * 2, distance)
      t.start()
      t.join()
      if distance > 1000:
        distance = 0
      time.sleep(3)



    