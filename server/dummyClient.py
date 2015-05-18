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
    conn = httplib.HTTPConnection("192.168.43.81:9000")
    conn.request("GET","/hello")
    res = conn.getresponse()
    print "request: ", self.id, " ---- ", res.status, res.reason


num = 0
while True:
  num = num + 1;
  t = MyThread(num)
  t.start()


    