import serial
import cat
import ft847
import time

io = serial.Serial('/dev/ttyUSB0', baudrate= 57600, bytesize=8, parity = 'N', stopbits=2)
catif = cat.Cat(io)
radio = ft847.Ft847(catif);
print radio.receiverStatus()
print radio.transmitStatus()
print radio.getMainVfoStatus()
radio.setFrequency(ft847.MAIN_VFO, 436123456.123)
radio.setFrequency(ft847.MAIN_VFO, 436000000.123)
radio.setMainVfoOperatingMode('CW')
#Below two might not work if sattellite mode is not enabled
#print radio.getSatRxVfoStatus()
#print radio.getSatTxVfoStatus()
radio.disconnect()

