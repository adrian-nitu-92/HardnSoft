import time
import BaseHTTPServer
import thread
import threading
import urlparse
import string

HOST_NAME = '192.168.43.81' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.

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
    
 
if __name__ == '__main__':
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      pass
  httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

