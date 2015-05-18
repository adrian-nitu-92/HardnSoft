import time
from threading import Thread, Lock
#This class is thread safe
#Each method is thread safe -> do not call them after lock.acquire()
class Structure:
  def __init__(self):
    self.hartRate = []
    # au fost trimise datele pana la lastSentHartRateIndex - 1
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