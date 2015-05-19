import plotly.plotly as py
from plotly.graph_objs import *
# (*) Useful Python/Plotly tools
import plotly.tools as tls   
import plotly
import numpy as np  # (*) numpy for math functions and arrays
from random import randint
import time

stream_ids = tls.get_credentials_file()['stream_ids']

stream_id = stream_ids[0]

# Make instance of stream id object 
stream = Stream(
    token=stream_id,  # (!) link stream id to 'token' key
    maxpoints=80      # (!) keep a max of 80 pts on screen
)

# Initialize trace of streaming plot by embedding the unique stream_id
trace1 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=stream         # (!) embed stream id, 1 per trace
)

trace2 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=stream         # (!) embed stream id, 1 per trace
)

data = Data([trace1])

# Add title to layout object
layout = Layout(title='Time Series')

# Make a figure object
fig = Figure(data=data, layout=layout)

# (@) Send fig to Plotly, initialize streaming plot, open new tab
unique_url = py.plot(fig, filename='s7_first-stream')

# (@) Make instance of the Stream link object, 
#     with same stream id as Stream id object
s = py.Stream(stream_id)

# (@) Open the stream
s.open()

x = 0
while True:
  x += 1
  y = randint(2,9)
  s.write(dict(x=x, y=y))
  time.sleep(0.5)
s.close()