import time
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import thread
import threading
import urlparse
import string
import sys, traceback
from structure import Structure

HOST_NAME = '192.168.1.132' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.
structure = Structure()

class MyHandler(BaseHTTPRequestHandler):
  def sendResponse(self, request, code, message):
    request.send_response(code)
    request.send_header("Content-type", "text")
    request.end_headers()
    request.wfile.write(message)
  def do_HEAD(self):
    pass
  def do_GET(self):
    """Respond to a GET request."""
    print "GET REQUEST: ", self.path
    if self.path == "/hello":
      try:
        self.sendResponse(self, 200, "my message")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if self.path == "/getChartsData":
      try:
        self.sendResponse(self, 200, structure.toString())
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    url = self.path
    parsed = urlparse.urlparse(url)
    if string.find(self.path, "/putHeartRate") != -1:
      try:
        value = float(urlparse.parse_qs(parsed.query)['value'][0])
        time = float(urlparse.parse_qs(parsed.query)['time'][0])
        structure.addHartRate(time, value)
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putNumSteps") != -1:
      try:
        value = float(urlparse.parse_qs(parsed.query)['value'][0])
        time = float(urlparse.parse_qs(parsed.query)['time'][0])
        structure.addNumSteps(time, value)
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putAirTemperature") != -1:
      try:
        value = float(urlparse.parse_qs(parsed.query)['value'][0])
        time = float(urlparse.parse_qs(parsed.query)['time'][0])
        structure.addTemperature(time, value)
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putHumidity") != -1:
      try:
        value = float(urlparse.parse_qs(parsed.query)['value'][0])
        time = float(urlparse.parse_qs(parsed.query)['time'][0])
        structure.addHumidity(time, value)
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Handle requests in a separate thread."""

isRunning = True
# ar trebui ca din 2 in 2 secunde sa se actualizeze logul
def LogData():
  if isRunning:
    #nu e bine:o sa scriu mereu date duplicate si nu vreau asta
    structure.logData()
    threading.Timer(10, LogData).start()

#./ngrok authtoken 25qDk5zVyA9FYfhf1bHq9_5eUvKuH647BZZsHBRvR3f
#./ngrok http -subdomain=randomtest 9999
if __name__ == '__main__':
  if len(sys.argv) == 2:
    PORT_NUMBER = int(sys.argv[1])
  if len(sys.argv) == 3:
    HOST_NAME = sys.argv[1]
    PORT_NUMBER = int(sys.argv[2])
  LogData()
  httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    isRunning = False
  httpd.server_close()
  #time.sleep(5)
  structure.clearLog()  
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

