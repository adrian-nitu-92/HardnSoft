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
    message = str(self.timestamp) + " " + self.checkpoint + " " + str(self.value) + " " + self.name
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

    self.treasure = []
    self.pertmanentTreasure = []
    self.mutexTreasure = Lock()

  def addTreasure(self, time, checkpoint, value, name):
    self.mutexTreasure.acquire()
    self.treasure.append([Treasure(time, checkpoint, value, name)])
    self.mutexTreasure.release()

  def addHartRate(self, time, value):
    self.mutexHartRate.acquire()
    self.hartRate.append([time, value])
    self.mutexHartRate.release()

  def addNumSteps(self, time, value):
    self.mutexNumSteps.acquire()
    if len(self.numSteps) == 0:
      self.numSteps.append([time, value])
    else:
      self.numSteps[0][0] = time
      self.numSteps[0][1] += value
    self.mutexNumSteps.release()

  def addTemperature(self, time, value):
    self.mutexTemperature.acquire()
    self.temperature.append([time, value])
    self.mutexTemperature.release()

  def addHumidity(self, time, value):
    self.mutexHumidity.acquire()
    self.humidity.append([time, value])
    self.mutexHumidity.release()

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
    self.clearNumSteps()
    self.clearTemperature()
    self.clearHumidity()
    self.clearTreasure()

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
    num = 0
    for rate in mylist:
      if num == 2:
        break
      num += 1
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