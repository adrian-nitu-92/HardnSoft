import time
import BaseHTTPServer
import thread
import threading
import urlparse
import string
import sys
from structure import Structure

HOST_NAME = '192.168.1.168' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.
structure = Structure()

class MyThread(threading.Thread):
  def __init__(self, request, code, message):
    threading.Thread.__init__(self)
    self.request = request
    self.code = code
    self.message = message

  def run(self):
    print "Start execute thread"
    self.sendResponse()
    print "End Thread"

  def sendResponse(self):
    print "... ", self.request.path
    self.request.send_response(self.code)
    self.request.send_header("Content-type", "text/html")
    self.request.end_headers()
    m = "<html><body><p>" +self.message +"</p></body></html>"
    self.request.wfile.write(m)

class ChartsDataThread(threading.Thread):
  def __init__(self, request, structure):
    threading.Thread.__init__(self)
    self.request = request
    self.structure = structure

  def run(self):
    print "Start ChartsDataThread"
    self.sendResponse(200, self.structure.toString())
    self.structure.clear()
    print "End Thread"

  def sendResponse(self, code, message):
    print "... ", self.request.path
    self.request.send_response(code)
    self.request.send_header("Content-type", "text")
    self.request.end_headers()
    self.request.wfile.write(message)

class PutDataThread(threading.Thread):
  def __init__(self, request, data, time, methodUpdate, methodClear, structure):
    threading.Thread.__init__(self)
    self.request = request
    self.data = data
    self.methodUpdate = methodUpdate
    self.methodClear = methodClear
    self.structure = structure
    self.time = time

  def run(self):
    print "Start ChartsDataThread"
    self.methodUpdate(self.time, self.data)
    self.sendResponse(200, "")
    print "##############33", self.structure.toString()
    print "End Thread"

  def sendResponse(self, code, message):
    print "... ", self.request.path
    self.request.send_response(code)
    self.request.send_header("Content-type", "text")
    self.request.end_headers()
    self.request.wfile.write(message)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(self):
    pass
  def do_GET(self):
    """Respond to a GET request."""

    print "GET REQUEST"
    print self.path
    if self.path == "/hello":
      print "call hello handler"
      t = MyThread(self, 200, "my message")
      t.start()
      t.join()
      return

    if self.path == "/getChartsData":
      print "call getChartsData"
      t = ChartsDataThread(self, structure)
      t.start()
      t.join()
      return

    url = self.path
    parsed = urlparse.urlparse(url)
    if string.find(self.path, "/putHeartRate") != -1:
      print "call putHartRate"
      value = float(urlparse.parse_qs(parsed.query)['value'][0])
      time = float(urlparse.parse_qs(parsed.query)['time'][0])
      t = PutDataThread(self, value, time, 
        structure.addHartRate, structure.clearHartRate,
        structure)
      t.start()
      t.join()
      return

    if string.find(self.path, "/putNumSteps") != -1:
      print "call putHartRate"
      value = float(urlparse.parse_qs(parsed.query)['value'][0])
      time = float(urlparse.parse_qs(parsed.query)['time'][0])
      t = PutDataThread(self, value, time, 
        structure.addNumSteps, structure.clearNumSteps, 
        structure)
      t.start()
      t.join()
      return
 
if __name__ == '__main__':
  if len(sys.argv) == 2:
    PORT_NUMBER = int(sys.argv[1])
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      pass
  httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

