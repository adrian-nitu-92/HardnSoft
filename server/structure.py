import time
from threading import Thread, Lock
import os
import urlparse


class Treasure:
  def __init__(self, timestamp, checkpoint, value, name):
    self.timestamp = timestamp
    self.checkpoint = checkpoint
    self.value = value
    self.name = name

  def toString(self):
    message = str(self.timestamp) + " " + str(self.checkpoint) + " " + self.value + " " + self.name
    return message

#This class is thread safe
#Each method is thread safe -> do not call them after lock.acquire()
class Structure:
  def __init__(self):
    self.timeStart = None
    self.mutexTimeStart = Lock()

    self.bodyTemperature = []
    self.mutexBodyTemperature = Lock()

    self.hartRate = []
    self.mutexHartRate = Lock()

    self.numSteps = []
    self.mutexNumSteps = Lock()

    self.distance = []
    self.mutexDistance = Lock()

    self.temperature = []
    self.mutexTemperature = Lock()

    self.humidity = []
    self.mutexHumidity = Lock()

    self.treasure = []
    self.pertmanentTreasure = []
    self.mutexTreasure = Lock()

    self.consumption = []
    self.mutexConsumption = Lock()

  def updateStart(self, parsed):
    self.mutexTimeStart.acquire()
    if self.timeStart == None:
      try:
        self.timeStart = float(urlparse.parse_qs(parsed.query)['time'][0])
      except:
        pass
    self.mutexTimeStart.release()

  def getBodyTemperature(self):
    self.mutexBodyTemperature.acquire()
    l = self.bodyTemperature
    self.mutexBodyTemperature.release()
    return l

  def getHartRate(self):
    self.mutexHartRate.acquire()
    l = self.hartRate
    self.mutexHartRate.release()
    return l

  def getNumSteps(self):
    self.mutexNumSteps.acquire()
    l = self.numSteps
    self.mutexNumSteps.release()
    return l

  def getDistance(self):
    self.mutexDistance.acquire()
    l = self.distance
    self.mutexDistance.release()
    return l

  def getTemperature(self):
    self.mutexTemperature.acquire()
    l = self.temperature
    self.mutexTemperature.release()
    return l

  def getHumidity(self):
    self.mutexHumidity.acquire()
    l = self.humidity
    self.mutexHumidity.release()
    return l

  def getTreasure(self):
    self.mutexTreasure.acquire()
    l = self.treasure
    self.mutexTreasure.release()
    return l

  def addBodyTemperature(self, rez):
    self.mutexBodyTemperature.acquire()
    self.bodyTemperature.append(rez)
    self.mutexBodyTemperature.release()

  def addHartRate(self, rez):
    self.mutexHartRate.acquire()
    self.hartRate.append(rez)
    self.mutexHartRate.release()

  def addNumSteps(self, rez):
    self.mutexNumSteps.acquire()
    self.numSteps = [rez]
    self.mutexNumSteps.release()

  def addDistance(self, rez):
    self.mutexDistance.acquire()
    self.distance.append(rez)
    self.mutexDistance.release()

  def addTemperature(self, rez):
    self.mutexTemperature.acquire()
    self.temperature.append(rez)
    self.mutexTemperature.release()

  def addHumidity(self, rez):
    self.mutexHumidity.acquire()
    self.humidity.append(rez)
    self.mutexHumidity.release()

  def addTreasure(self, time, checkpoint, value, name):
    self.mutexTreasure.acquire()
    self.treasure.append(Treasure(time, checkpoint, value, name))
    self.mutexTreasure.release()

  def addConsumption(self, rez):
    self.mutexConsumption.acquire()
    self.consumption.append(rez)
    self.mutexConsumption.release()

  def clear(self):
    self.logData()

  def toString(self):
    #adaugam body temperature: 
    message = self._toString("bodytemperature",
      self.bodyTemperature,
      self.mutexBodyTemperature)
    # adaugam hartRate:
    message += self._toString("heartrate", 
      self.hartRate, 
      self.mutexHartRate)
    #adaugam numSteps:
    message += self._toString("numsteps",
      self.numSteps,
      self.mutexNumSteps)
    #adaugam distance: 
    message += self._toString("distance",
      self.distance,
      self.mutexDistance)
    #adaugam temperature: 
    message += self._toString("airtemperature",
      self.temperature,
      self.mutexTemperature)
    #adaugam temperature: 
    message += self._toString("humidity",
      self.humidity,
      self.mutexHumidity)
    message += self._toStringTreasure("treasure",
      self.treasure,
      self.mutexTreasure)
    #adaugam compumption: 
    message += self._toString("consumption",
      self.consumption,
      self.mutexConsumption)
    self.clear()
    return message

  def _toStringTreasure(self, key, mylist, mutex):
    mutex.acquire()
    message = key + "="
    for rate in mylist:
      message += rate.toString() + "|"
    # delimitator
    message += ";"
    mutex.release()
    return message

  def _toString(self, key, mylist, mutex):
    mutex.acquire()
    message = key + "="
    for rate in mylist:
      message += str(rate[0]) + " " + str(rate[1]) + "|"
    # delimitator
    message += ";"
    mutex.release()
    return message

  def logData(self):
    # log body temperature: 
    self.mutexBodyTemperature.acquire()
    self._logData("bodyTemperature",
      self.humidity)
    self.bodyTemperature = []
    self.mutexBodyTemperature.release()

    # log hartRate:
    self.mutexHartRate.acquire()
    self._logData("heartrate", 
      self.hartRate)
    self.hartRate = []
    self.mutexHartRate.release()

    # log numSteps: 
    self.mutexNumSteps.acquire()
    self._logData("numsteps",
      self.numSteps)
    self.numSteps = []
    self.mutexNumSteps.release()

    # log distance: 
    self.mutexDistance.acquire()
    self._logData("distance",
      self.humidity)
    self.distance = []
    self.mutexDistance.release()

    # log airtemperature:
    self.mutexTemperature.acquire() 
    self._logData("airTemperature",
      self.temperature)
    self.temperature = []
    self.mutexTemperature.release()

    # log humidity: 
    self.mutexHumidity.acquire()
    self._logData("humidity",
      self.humidity)
    self.humidity = []
    self.mutexHumidity.release()

    # log treasure:
    self.mutexTreasure.acquire()
    for t in self.treasure:
      self.pertmanentTreasure.append(t)
    self.treasure = []
    self.mutexTreasure.release()

    # log consumption: 
    self.mutexConsumption.acquire()
    self._logData("consumption",
      self.consumption)
    self.consumption = []
    self.mutexConsumption.release()

  def _logData(self, key, mylist):
    with open(key, "a") as myfile:
      myfile.write(self.serializeList(mylist))

  def serializeList(self, mylist):
    message = ""
    for elem in mylist:
      message += str(elem[0]) + " " + str(elem[1]) + ";\n"
    return message

  def logTreasure(self):
    self.mutexTreasure.acquire()
    message = ""
    for elem in self.pertmanentTreasure:
      message += str(elem.timestamp) + " " + str(elem.checkpoint) + " " + str(elem.value) + " " + elem.name + ";\n"
    self.mutexTreasure.release()
    with open("treasure", "a") as myfile:
      myfile.write(message)

  def clearLog(self):
    self._clearData("bodyTemperature", 
      self.mutexBodyTemperature)
    self._clearData("heartrate", 
      self.mutexHartRate)
    self._clearData("numsteps",
      self.mutexNumSteps)
    self._clearData("distance", 
      self.mutexDistance)
    self._clearData("airtemperature",
      self.mutexTemperature)
    self._clearData("humidity",
      self.mutexHumidity)
    self._clearData("treasure",
      self.mutexTreasure)

  def _clearData(self, key, mutex):
    mutex.acquire()
    try:
      os.remove(key)
    except:
      pass
    mutex.release()