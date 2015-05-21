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
    from random import randint
    conn = httplib.HTTPConnection(ROOT)
    conn.request("GET","/putBodyTemp?value="+str(randint(-100,100))+"&time="+str(int(time.time()*1000)+5)+"&statie=x")
    res = conn.getresponse()
    print "putBodyTemp: ", self.id, " ---- ", res.status, res.reason

    conn.request("GET","/putHeartRate?value="+str(self.id)+"&time="+str(int(time.time()*1000)+5)+"&statie=x")
    res = conn.getresponse()
    print "putHeartRate: ", self.id, " ---- ", res.status, res.reason

    conn.request("GET","/putNumSteps?value="+str(self.nrSteps)+"&time="+str(int(time.time()*1000)+5)+"&statie=x")
    res = conn.getresponse()
    print " putNumSteps: ", self.id, " ---- ", res.status, res.reason

    conn.request("GET","/putDistance?value="+str(self.distance)+"&time="+str(int(time.time()*1000)+5)+"&statie=x")
    res = conn.getresponse()
    print "putDistance: ", self.id, " ---- ", res.status, res.reason

    conn.request("GET","/putAirTemp?value="+str(randint(2,9))+"&time="+str(int(time.time()*1000)+5)+"&statie=x")
    res = conn.getresponse()
    print "putAirTemp: ", self.id, " ---- ", res.status, res.reason

    conn.request("GET","/putHumidity?value="+str(randint(-100,100))+"&time="+str(int(time.time()*1000)+5)+"&statie=x")
    res = conn.getresponse()
    print "putHumidity: ", self.id, " ---- ", res.status, res.reason
    
    conn.request("GET","/putTreasure?time="+str(int(time.time()*1000)+5)+"&checkpoint="+str(randint(0,10))+"&value="+str(randint(-100,100))+"&name=dummy")
    res = conn.getresponse()
    print "putTreasure: ", self.id, " ---- ", res.status, res.reason

    conn.request("GET","/putConsumption?value="+str(randint(-100,100))+"&time="+str(int(time.time()*1000)+5)+"&statie=x")
    res = conn.getresponse()
    print "putConsumption: ", self.id, " ---- ", res.status, res.reason
    print "..............................................................."

if __name__ == '__main__':
  print len(sys.argv)
  l = len(sys.argv)
  if l == 2:
    ROOT = sys.argv[1]
  else:
    ROOT = sys.argv[1] + ":" + sys.argv[2]

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



    