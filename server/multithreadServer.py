import time
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import thread
import threading
import urlparse
import string
import sys, traceback
from structure import Structure


import plotly.plotly as py
from plotly.graph_objs import *
# (*) Useful Python/Plotly tools
import plotly.tools as tls   
import plotly
import numpy as np

HOST_NAME = '192.168.1.168' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.
structure = Structure()


class ChartData:
  def __init__(self, stream_id, stream, trace, data, layout, fig, unique_url, s, method):
    self.stream_id = stream_id
    self.stream = stream
    self.trace = trace
    self.data = data 
    self.layout = layout 
    self.fig = fig
    self.unique_url = unique_url
    self.s = s
    self.method = method

class ChartRender(threading.Thread):
  def __init__(self, chart):
    threading.Thread.__init__(self)
    self.chart = chart

  def run(self):
    self.chart.s.open()
    while True:
      points = self.chart.method
      for point in points:
        self.chart.s.write(dict(x=point[0], y=point[1]))
      time.sleep(0.5)
    self.chart.s.close()


class Chart:
  def __init__(self):
    stream_ids = tls.get_credentials_file()['stream_ids']
    self.charts = []
    methods = [structure.getHartRate(), structure.getNumSteps(), structure.getTemperature(), structure.getHumidity()]
    title = ["Hart Rate", "Steps", "Air Temperature", "Humidity"]
    filename = ["HartRate", "Steps", "AirTemperature", "Humidity"]
    num = 0
    for stream_id in stream_ids:
      # Make instance of stream id object 
      stream = Stream(
        token=stream_id,  # (!) link stream id to 'token' key
        maxpoints=80      # (!) keep a max of 80 pts on screen
      )
      # Initialize trace of streaming plot by embedding the unique stream_id
      trace = Scatter(
          x=[],
          y=[],
          mode='lines+markers',
          stream=stream         # (!) embed stream id, 1 per trace
      )
      data = Data([trace])
      # Add title to layout object
      layout = Layout(title=title[num])

      # Make a figure object
      fig = Figure(data=data, layout=layout)

      # (@) Send fig to Plotly, initialize streaming plot, open new tab
      unique_url = py.plot(fig, filename=filename[num])

      # (@) Make instance of the Stream link object, 
      #     with same stream id as Stream id object
      s = py.Stream(stream_id)
      self.charts.append(ChartData(stream_id, stream, trace, data, layout, fig, unique_url, s, methods[num]))
      num = num + 1

  def run(self):
    t = []
    for chart in self.charts:
      tr = ChartRender(chart)
      t.append(tr)
      tr.start()

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
        m = structure.toString()
        print "-------------------------",m, "-------------" 
        self.sendResponse(self, 200, m)
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

    if string.find(self.path, "/putTreasure") != -1:
      try:
        time = float(urlparse.parse_qs(parsed.query)['time'][0])
        checkpoint = float(urlparse.parse_qs(parsed.query)['checkpoint'][0])
        value = float(urlparse.parse_qs(parsed.query)['value'][0])
        name = urlparse.parse_qs(parsed.query)['name'][0]
        structure.addTreasure(time, checkpoint, value, name)
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putBodyTemperature") != -1:
      try:
        time = float(urlparse.parse_qs(parsed.query)['time'][0])
        value = float(urlparse.parse_qs(parsed.query)['value'][0])
        structure.addBodyTemperature(time, value)
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putConsumption") != -1:
      try:
        time = float(urlparse.parse_qs(parsed.query)['time'][0])
        value = float(urlparse.parse_qs(parsed.query)['value'][0])
        structure.addConsumption(time, value)
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putDistance") != -1:
      try:
        time = float(urlparse.parse_qs(parsed.query)['time'][0])
        value = float(urlparse.parse_qs(parsed.query)['value'][0])
        structure.addDistance(time, value)
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Handle requests in a separate thread."""

isRunning = True

#./ngrok authtoken 25qDk5zVyA9FYfhf1bHq9_5eUvKuH647BZZsHBRvR3f
#./ngrok http -subdomain=randomtest 9999
if __name__ == '__main__':
  structure.clearLog()
  if len(sys.argv) == 2:
    PORT_NUMBER = int(sys.argv[1])
  if len(sys.argv) == 3:
    HOST_NAME = sys.argv[1]
    PORT_NUMBER = int(sys.argv[2])
  #LogData()
  #Chart().run()
  httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    isRunning = False
  httpd.server_close()
  structure.logTreasure()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

