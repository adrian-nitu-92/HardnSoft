from threading import Thread, Lock
from datetime import datetime

class Treasure:
  def __init__(self, timestamp, value, checkpoint, name):
    self.timestamp = timestamp
    self.checkpoint = checkpoint
    self.value = value
    self.name = name
  def csvString(self):
    ts = datetime.fromtimestamp(self.timestamp/1000.0).strftime('%d.%m.%Y-%H.%M.%S')
    return ts + "," + self.value
  def toString(self):
    message = str(self.timestamp) + " " + str(self.checkpoint) + " " + self.value + " " + self.name
    return message


class BioData:
  def __init__(self, bodyTemperature, heartRate, numSteps, distance):
    self.bodyTemperature = bodyTemperature
    self.heartRate = heartRate
    self.numSteps = numSteps
    self.distance = distance
    self.timestamp = None

  def csvString(self):
    if not self.timestamp is None:
      ts = datetime.fromtimestamp(self.timestamp/1000.0).strftime('%d.%m.%Y-%H.%M.%S')
    else: 
      ts = ""
    return "  Bio-Data," + ts + "\n" + \
      "    Body Temperature[*C],," + str(self.bodyTemperature) + "\n" + \
      "    Pulse Rate[bpm],," + str(self.heartRate) + "\n" + \
      "    Number of steps,," + str(self.numSteps) + "\n" + \
      "    Distance traveled,," + str(self.distance) + "\n"

class EnvData:
  def __init__(self, airTemp, humidity):
    self.airTemp = airTemp
    self.humidity = humidity
    self.timestamp = None

  def csvString(self):
    if not self.timestamp is None:
      ts = datetime.fromtimestamp(self.timestamp/1000.0).strftime('%d.%m.%Y-%H.%M.%S')
    else:
      ts = ""
    return "  Environment Data," +  ts + "\n" \
      "    Air Temperature[*C],," + str(self.airTemp) + "\n" + \
      "    Humidity[%],," + str(self.humidity) + "\n"

class TreasureRecords:
  def __init__(self):
    self.numTreasures = 0
    self.treasuresList = []

  def csvString(self):
    timestamp = ""
    if len(self.treasuresList) > 0 and not self.treasuresList[0].timestamp is None:
      timestamp = datetime.fromtimestamp(self.treasuresList[0].timestamp/1000.0).strftime('%d.%m.%Y-%H.%M.%S')
    message = "  Treasure records," + timestamp + "\n    Number of treasures," + str(self.numTreasures) + "\n"
    num = 1
    for treasure in self.treasuresList:
      message += "    Treasure " + str(num) + "," + treasure.csvString() + "\n"
    return message

class Station:
  def __init__(self, bioData, envData, treasureRec, index, timestamp):
    self.bioData = bioData
    self.envData = envData
    self.treasureRec = treasureRec
    self.lock = Lock()
    self.index = index
    self.timestamp = timestamp

  def csvString(self):
    if not self.timestamp is None:
      ts = datetime.fromtimestamp(self.timestamp/1000.0).strftime('%d.%m.%Y-%H.%M.%S')
    else:
      ts = ""
    message = ""
    if self.index == 0:
      message += "Start information,"
    elif self.index == 6:
      message += "Finish line,"
    else:
      message += "Station " + str(self.index) + ","
    self.bioData.timestamp = self.timestamp
    self.envData.timestamp = self.timestamp
    return message + ts + "\n" + \
      self.bioData.csvString() + \
      self.envData.csvString() + \
      self.treasureRec.csvString() + "\n"

