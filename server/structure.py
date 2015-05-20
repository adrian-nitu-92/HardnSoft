import time
from threading import Thread, Lock
import os


class Treasure:
  def __init__(self, timestamp, checkpoint, value, name):
    self.timestamp = timestamp
    self.checkpoint = checkpoint
    self.value = value
    self.name = name

  def toString(self):
    message = str(self.timestamp) + " " + str(self.checkpoint) + " " + str(self.value) + " " + self.name
    return message

#This class is thread safe
#Each method is thread safe -> do not call them after lock.acquire()
class Structure:
  def __init__(self):
    self.hartRate = []
    self.mutexHartRate = Lock()

    self.numSteps = []
    self.mutexNumSteps = Lock()

    self.temperature = []
    self.mutexTemperature = Lock()

    self.humidity = []
    self.mutexHumidity = Lock()

    self.bodyTemperature = []
    self.mutexBodyTemperature = Lock()

    self.consumption = []
    self.mutexConsumption = Lock()

    self.distance = []
    self.mutexDistance = Lock()

    self.treasure = []
    self.pertmanentTreasure = []
    self.mutexTreasure = Lock()

  def getHumidity(self):
    self.mutexHumidity.acquire()
    l = self.humidity
    self.mutexHumidity.release()
    return l

  def getTemperature(self):
    self.mutexTemperature.acquire()
    l = self.temperature
    self.mutexTemperature.release()
    return l

  def getNumSteps(self):
    self.mutexNumSteps.acquire()
    l = self.numSteps
    self.mutexNumSteps.release()
    return l

  def getHartRate(self):
    self.mutexHartRate.acquire()
    l = self.hartRate
    self.mutexHartRate.release()
    return l

  def addTreasure(self, time, checkpoint, value, name):
    self.mutexTreasure.acquire()
    self.treasure.append(Treasure(time, checkpoint, value, name))
    self.mutexTreasure.release()

  def addDistance(self, rez):
    self.mutexDistance.acquire()
    self.distance.append(rez)
    self.mutexDistance.release()

  def addConsumption(self, rez):
    self.mutexConsumption.acquire()
    self.consumption.append(rez)
    self.mutexConsumption.release()
  
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
    if len(self.numSteps) == 0:
      self.numSteps.append(rez)
    else:
      self.numSteps[0][0] = rez[0]
      self.numSteps[0][1] += rez[1]
      try:
        self.numSteps[0][2] = rez[2]
      except:
        pass
    self.mutexNumSteps.release()

  def addTemperature(self, rez):
    self.mutexTemperature.acquire()
    self.temperature.append(rez)
    self.mutexTemperature.release()

  def addHumidity(self, rez):
    self.mutexHumidity.acquire()
    self.humidity.append(rez)
    self.mutexHumidity.release()

  def clearDistance(self):
    self.mutexDistance.acquire()
    self.distance = []
    self.mutexDistance.release()

  def clearConsumption(self):
    self.mutexConsumption.acquire()
    self.consumption = []
    self.mutexConsumption.release()
  
  def clearBodyTemperature(self):
    self.mutexBodyTemperature.acquire()
    self.bodyTemperature = []
    self.mutexBodyTemperature.release()

  def clearTreasure(self):
    self.mutexTreasure.acquire()
    for i in self.treasure:
      self.pertmanentTreasure.append(i)
    self.treasure = []
    self.mutexTreasure.release()

  def clearHartRate(self):
    self.mutexHartRate.acquire()
    self.hartRate = []
    self.mutexHartRate.release()

  def clearNumSteps(self):
    self.mutexNumSteps.acquire()
    self.numSteps = []
    self.mutexNumSteps.release()

  def clearTemperature(self):
    self.mutexTemperature.acquire()
    self.temperature = []
    self.mutexTemperature.release()

  def clearHumidity(self):
    self.mutexHumidity.acquire()
    self.humidity = []
    self.mutexHumidity.release()

  def clear(self):
    self.logData()
    self.clearHartRate()
    #self.clearNumSteps()
    self.clearTemperature()
    self.clearHumidity()
    self.clearTreasure()
    self.clearBodyTemperature()
    self.clearConsumption()
    self.clearDistance()

  def toString(self):
    # adaugam hartRate:
    message = self._toString("heartrate", 
      self.hartRate, 
      self.mutexHartRate)
    #adaugam numSteps:
    message += self._toString("numsteps",
      self.numSteps,
      self.mutexNumSteps)
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
    #adaugam body temperature: 
    message += self._toString("bodytemperature",
      self.bodyTemperature,
      self.mutexBodyTemperature)
    #adaugam compumption: 
    message += self._toString("comsumption",
      self.consumption,
      self.mutexConsumption)
    #adaugam distance: 
    message += self._toString("distance",
      self.distance,
      self.mutexDistance)
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

    # log temperature:
    self.mutexTemperature.acquire() 
    self._logData("airtemperature",
      self.temperature)
    self.temperature = []
    self.mutexTemperature.release()

    # log temperature: 
    self.mutexHumidity.acquire()
    self._logData("humidity",
      self.humidity)
    self.humidity = []
    self.mutexHumidity.release()

    print self.humidity

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
      message += elem.timestamp + " " + elem.checkpoint + " " + elem.value + " " + self.name + ";\n"
    self.mutexTreasure.release()
    with open("treasure", "a") as myfile:
      myfile.write(message)

  def clearLog(self):
    # delete hartRate:
    self._clearData("heartrate", 
      self.mutexHartRate)
    # log numSteps: 
    self._clearData("numsteps",
      self.mutexNumSteps)
    # log temperature: 
    self._clearData("airtemperature",
      self.mutexTemperature)
    # log temperature: 
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