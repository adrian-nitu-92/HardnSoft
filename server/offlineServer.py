import os
import time
import sys

HOST_NAME = '192.168.43.81' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.

nrMountari = 0
device_name = "/media/ioana/IOANA" 
if __name__ == '__main__':

  if len(sys.argv) >= 2:
    device_name = sys.argv[1]

  while True:
    while not os.path.ismount(device_name):
      pass

    nrMountari = nrMountari + 1
    print "device: ", device_name, "mountarea nr: ", nrMountari
    while os.path.ismount(device_name):
      pass
    print device_name, " disconnected"

