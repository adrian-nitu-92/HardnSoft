import httplib
import thread
import time
import threading
import sys


HOST_NAME = '192.168.1.168' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.
ROOT = ""

class MyThread(threading.Thread):
  def __init__(self, id):
    threading.Thread.__init__(self)
    self.id = id

  def run(self):
    print "Start execute thread ", self.id
    self.sendRequest()
    print "End Thread ",self.id

  def sendRequest(self):
    conn = httplib.HTTPConnection(ROOT)
    conn.request("GET","/putHeartRate?value="+str(self.id)+"&time="+str(time.time()))
    res = conn.getresponse()
    #print "request: ", self.id, " ---- ", res.status, res.reason
    conn.request("GET","/putNumSteps?value="+str(self.id)+"&time="+str(time.time()))
    res = conn.getresponse()
    from random import randint
    conn.request("GET","/putTemperature?value="+str(randint(2,9))+"&time="+str(time.time()))
    res = conn.getresponse()
    conn.request("GET","/putHumidity?value="+str(randint(-100,100))+"&time="+str(time.time()))
    res = conn.getresponse()
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

  while True:
    for i in xrange(10):
      t = MyThread(i+1)
      t.start()
      t.join()
      #time.sleep(0.5)



    