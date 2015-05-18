import time
from threading import Thread, Lock
#This class is thread safe
class Structure:
  def __init__(self):
    self.hartRate = []
    # au fost trimise datele pana la lastSentHartRateIndex - 1
    self.lastSentHartRateIndex = 0
    self.mutexHartRate = Lock()

    self.numSteps = []
    self.lastSentNumStepsIndex = 0
    self.mutexNumSteps = Lock()

  def addHartRate(self, time, value):
    self.mutexHartRate.acquire()
    self.hartRate.append([time, value])
    self.mutexHartRate.release()


  def addNumSteps(self, time, value):
    self.mutexNumSteps.acquire()
    self.numSteps.append([time, value])
    self.mutexNumSteps.release()

  def clearHartRate(self):
    self.mutexHartRate.acquire()
    self.hartRate = []
    self.mutexHartRate.release()


  def clearNumSteps(self):
    self.mutexNumSteps.acquire()
    self.numSteps = []
    self.mutexNumSteps.release()

  def clear(self):
    self.clearHartRate()
    self.clearNumSteps()

  def toString(self):
    # adaugam hartRate:
    message = self._toString("heartrate", 
      self.hartRate, 
      self.mutexHartRate)
    #self.clearHartRate()
    #adaugam numSteps: 
    message += self._toString("numsteps",
      self.numSteps,
      self.mutexNumSteps)
    #self.clearNumSteps()
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