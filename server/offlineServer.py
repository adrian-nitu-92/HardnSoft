import os
import time
import sys

HOST_NAME = '192.168.43.81' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.

nrMountari = 0
device_name = "/media/ioana/IOANA" 

def read_sd():
  # ls recursiv pe fisierele de pe card
  files = os.listdir(device_name)
  #ignore files starting with '.' using list comprehension
  files=[filename for filename in files if filename[0] != '.']
  print files

  for filename in files:
    try: #exceptions
      #Get all the file info
      stat_info=os.lstat(filename)
    except:
      sys.stderr.write("%s: No such file or directory\n" % filename)
      continue


if __name__ == '__main__':

  if len(sys.argv) >= 2:
    device_name = sys.argv[1]

  while True:
    while not os.path.ismount(device_name):
      pass

    nrMountari = nrMountari + 1
    print "device: ", device_name, "mountarea nr: ", nrMountari
    read_card = True
    while os.path.ismount(device_name):
      if read_card:
        read_sd()
        read_card = False;
        time.sleep(10) # wait 10 seconds
        read_card = True
      
    print device_name, " disconnected"

