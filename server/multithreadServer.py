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
isRunning = True


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
    self.chart.s.open()

  def run(self):
    self.chart.s.open()
    maxTimestap = 0
    while isRunning:
      inputPoints = self.chart.method()
      inputPoints.sort(key=lambda tup: tup[0])
      points = [point for point in inputPoints if point[0] > maxTimestap]
      if (len(points)): 
        maxTimestap = points[len(points)-1][0]
        for point in points:
          self.chart.s.write(dict(x=point[0], y=point[1]))
      time.sleep(1)
    self.chart.s.close()

class Chart:
  def __init__(self):
    stream_ids = tls.get_credentials_file()['stream_ids']
    self.charts = []
    methods = [structure.getBodyTemperature, 
      structure.getHartRate,
      structure.getNumSteps,
      structure.getDistance,
      structure.getTemperature,
      structure.getHumidity,
      structure.getTreasure]
    title = ["Body Temperature", "Heart Rate", "Steps", "Distance", "Air Temperature", "Humidity", "Treasure"]
    filename = ["BodyTemperature", "HeartRate", "Steps", "Distance", "AirTemperature", "Humidity", "Treasure"]
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
      layout = Layout(
        title=title[num]
          #xaxis=XAxis(
          #autotick=False,
          #ticks='outside',
          #tick0=0,
          #dtick=0.25,
          #showgrid=True,
          #zeroline=True,
          #showline=True,
          #mirror='ticks',
          #gridcolor='#bdbdbd',
          #gridwidth=2,
          #zerolinecolor='#969696',
          #zerolinewidth=4,
          #linecolor='#636363',
          #linewidth=6),
        #yaxis=YAxis(
          #showgrid=True,
          #zeroline=True,
          #showline=True,
          #mirror='ticks',
          #gridcolor='#bdbdbd',
          #gridwidth=2,
          #zerolinecolor='#969696',
          #zerolinewidth=4,
          #linecolor='#636363',
          #linewidth=6)
      )

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
    num = 0
    for chart in self.charts:
      if num==6:
        continue
      num += 1
      tr = ChartRender(chart)
      t.append(tr)
      tr.start()

class MyHandler(BaseHTTPRequestHandler):
  def sendResponse(self, request, code, message):
    request.send_response(code)
    request.send_header("Content-type", "text")
    request.end_headers()
    request.wfile.write(message)

  def parse(self, parsed):
    rez = []
    try:
      rez.append(float(urlparse.parse_qs(parsed.query)['time'][0]))
    except:
      pass
    try:
      rez.append(float(urlparse.parse_qs(parsed.query)['value'][0]))
    except:
      pass
    try:
      rez.append(urlparse.parse_qs(parsed.query)['statie'][0])
    except:
      pass
    return rez

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

    if string.find(self.path, "/putBodyTemp") != -1:
      try:
        structure.addBodyTemperature(self.parse(parsed))
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putHeartRate") != -1:
      try:
        structure.addHartRate(self.parse(parsed))
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putNumSteps") != -1:
      try:
        structure.addNumSteps(self.parse(parsed))
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putDistance") != -1:
      try:
        structure.addDistance(self.parse(parsed))
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putAirTemp") != -1:
      try:
        structure.addTemperature(self.parse(parsed))
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    if string.find(self.path, "/putHumidity") != -1:
      try:
        structure.addHumidity(self.parse(parsed))
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

    if string.find(self.path, "/putConsumption") != -1:
      try:
        structure.addConsumption(self.parse(parsed))
        self.sendResponse(self, 200, "")
      except:
        self.sendResponse(self, 400, "")
        traceback.print_exc(file=sys.stdout)
      return

    
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Handle requests in a separate thread."""

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
  Chart().run()
  httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    isRunning = False
  httpd.server_close()
  structure.logTreasure()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

