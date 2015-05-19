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
    self.sendResponse()

  def sendResponse(self):
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
    self.sendResponse(200, self.structure.toString())
    self.structure.clear()

  def sendResponse(self, code, message):
    self.request.send_response(code)
    self.request.send_header("Content-type", "text")
    self.request.end_headers()
    self.request.wfile.write(message)

class PutDataThread(threading.Thread):
  def __init__(self, request, data, time, methodUpdate, structure):
    threading.Thread.__init__(self)
    self.request = request
    self.data = data
    self.methodUpdate = methodUpdate
    self.structure = structure
    self.time = time

  def run(self):
    self.methodUpdate(self.time, self.data)
    self.sendResponse(200, "")

  def sendResponse(self, code, message):
    self.request.send_response(code)
    self.request.send_header("Content-type", "text")
    self.request.end_headers()
    self.request.wfile.write(message)
    print message

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(self):
    pass
  def do_GET(self):
    """Respond to a GET request."""
    print "GET REQUEST: ", self.path
    if self.path == "/hello":
      t = MyThread(self, 200, "my message")
      t.start()
      t.join()
      return

    if self.path == "/getChartsData":
      t = ChartsDataThread(self, structure)
      t.start()
      t.join()
      return

    url = self.path
    parsed = urlparse.urlparse(url)
    if string.find(self.path, "/putHeartRate") != -1:
      value = float(urlparse.parse_qs(parsed.query)['value'][0])
      time = float(urlparse.parse_qs(parsed.query)['time'][0])
      t = PutDataThread(self, value, time, 
        structure.addHartRate,
        structure)
      t.start()
      t.join()
      return

    if string.find(self.path, "/putNumSteps") != -1:
      value = float(urlparse.parse_qs(parsed.query)['value'][0])
      time = float(urlparse.parse_qs(parsed.query)['time'][0])
      t = PutDataThread(self, value, time, 
        structure.addNumSteps, 
        structure)
      t.start()
      t.join()
      return

    if string.find(self.path, "/putTemperature") != -1:
      value = float(urlparse.parse_qs(parsed.query)['value'][0])
      time = float(urlparse.parse_qs(parsed.query)['time'][0])
      t = PutDataThread(self, value, time, 
        structure.addTemperature, structure)
      t.start()
      t.join()
      return

    if string.find(self.path, "/putHumidity") != -1:
      value = float(urlparse.parse_qs(parsed.query)['value'][0])
      time = float(urlparse.parse_qs(parsed.query)['time'][0])
      t = PutDataThread(self, value, time, 
        structure.addHumidity, structure)
      t.start()
      t.join()
      return
 
if __name__ == '__main__':
  if len(sys.argv) == 2:
    PORT_NUMBER = int(sys.argv[1])
  if len(sys.argv) == 3:
    HOST_NAME = sys.argv[1]
    PORT_NUMBER = int(sys.argv[2])
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      pass
  httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

