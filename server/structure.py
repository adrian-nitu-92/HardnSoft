import time
from threading import Thread, Lock
import os
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

  def addHartRate(self, time, value):
    self.mutexHartRate.acquire()
    self.hartRate.append([time, value])
    self.mutexHartRate.release()


  def addNumSteps(self, time, value):
    self.clearNumSteps()
    self.mutexNumSteps.acquire()
    self.numSteps.append([time, value])
    self.mutexNumSteps.release()

  def addTemperature(self, time, value):
    self.mutexTemperature.acquire()
    self.temperature.append([time, value])
    self.mutexTemperature.release()

  def addHumidity(self, time, value):
    self.mutexHumidity.acquire()
    self.humidity.append([time, value])
    self.mutexHumidity.release()

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
    self.clearHartRate()
    self.clearNumSteps()
    self.clearTemperature()
    self.clearHumidity()

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
    message += self._toString("temperature",
      self.temperature,
      self.mutexTemperature)
    #adaugam temperature: 
    message += self._toString("humidity",
      self.humidity,
      self.mutexHumidity)
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
    self._logData("heartrate", 
      self.hartRate, 
      self.mutexHartRate)
    # log numSteps: 
    self._logData("numsteps",
      self.numSteps,
      self.mutexNumSteps)
    # log temperature: 
    self._logData("temperature",
      self.temperature,
      self.mutexTemperature)
    # log temperature: 
    self._logData("humidity",
      self.humidity,
      self.mutexHumidity)

  def _logData(self, key, mylist, mutex):
    mutex.acquire()
    with open(key, "a") as myfile:
      myfile.write(self.serializeList(mylist))
    mutex.release()

  def serializeList(self, mylist):
    message = ""
    for elem in mylist:
      message += str(elem[0]) + " " + str(elem[1]) + ";\n"
    return message

  def clearLog(self):
    # delete hartRate:
    self._clearData("heartrate", 
      self.mutexHartRate)
    # log numSteps: 
    self._clearData("numsteps",
      self.mutexNumSteps)
    # log temperature: 
    self._clearData("temperature",
      self.mutexTemperature)
    # log temperature: 
    self._clearData("humidity",
      self.mutexHumidity)

  def _clearData(self, key, mutex):
    mutex.acquire()
    os.remove(key)
    mutex.release()