"""
MOT streaming sequence 
FIO0-7 resolution: 10 us

"""
import sys
import time
from labjack import ljm
from numpy import genfromtxt

def write_bufferLJ(handle,estado):
    ljm.eWriteName(handle, "STREAM_OUT0_BUFFER_U16", estado)
    return;
    
t_time = 10  #Tiempo total en segundos. 
    
datos = genfromtxt('ctrl.csv',delimiter=',')

datos = datos[:,0]
datos = datos.astype(int)


MAX_REQUESTS = 20  # The number of eStreamRead calls that will be performed.

# Open first found LabJack
handle = ljm.openS("ANY", "ANY", "ANY")  # Any device, Any connection, Any identifier
#handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier
#handle = ljm.openS("T4", "ANY", "ANY")  # T4 device, Any connection, Any identifier
#handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")  # Any device, Any connection, Any identifier

info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
      "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
      (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

deviceType = info[0]

# Setup Stream Out
OUT_NAMES = ["FIO"]
NUM_OUT_CHANNELS = len(OUT_NAMES)
#outAddress = ljm.nameToAddress(OUT_NAMES[0])[0]
outAddress = 2500

# Allocate memory for the stream-out buffer
ljm.eWriteName(handle, "STREAM_OUT0_TARGET", outAddress)
ljm.eWriteName(handle, "STREAM_OUT0_BUFFER_SIZE", 512)
ljm.eWriteName(handle, "STREAM_OUT0_ENABLE", 1)

# Write values to the stream-out buffer
ljm.eWriteName(handle, "STREAM_OUT0_LOOP_SIZE", len(datos))
for i in range(1,len(datos)-1):
    write_bufferLJ(handle,datos[i])
    

ljm.eWriteName(handle, "STREAM_OUT0_SET_LOOP", 1)

print("STREAM_OUT0_BUFFER_STATUS = %f" % (ljm.eReadName(handle, "STREAM_OUT0_BUFFER_STATUS")))

# Stream Configuration
NUM_IN_CHANNELS = 0

TOTAL_NUM_CHANNELS = NUM_IN_CHANNELS + NUM_OUT_CHANNELS

# Add positive channels to scan list
#aScanList = ljm.namesToAddresses(NUM_IN_CHANNELS, POS_IN_NAMES)[0]
scanRate = 100000
scansPerRead = 60

# Add the scan list outputs to the end of the scan list.
# STREAM_OUT0 = 4800, STREAM_OUT1 = 4801, etc.
#aScanList.extend([4800])  # STREAM_OUT0
aScanList=([4800])  # STREAM_OUT0
# If we had more STREAM_OUTs
#aScanList.extend([4801])  # STREAM_OUT1
#aScanList.extend([4802])  # STREAM_OUT2
#aScanList.extend([4803])  # STREAM_OUT3

try:


    # Configure and start stream
    scanRate = ljm.eStreamStart(handle, scansPerRead, TOTAL_NUM_CHANNELS, aScanList, scanRate)

 
except ljm.LJMError:
    ljme = sys.exc_info()[1]
    print(ljme)
except Exception:
    e = sys.exc_info()[1]
    print(e)

print("\nStreaming")
time.sleep(t_time)

try:
    print("\nStop Stream")
    ljm.eStreamStop(handle)
except ljm.LJMError:
    ljme = sys.exc_info()[1]
    print(ljme)
except Exception:
    e = sys.exc_info()[1]
    print(e)

# Close handle
ljm.close(handle)
