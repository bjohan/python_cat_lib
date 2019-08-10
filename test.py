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
#radio.setFrequency(ft847.MAIN_VFO, 123436123456.123)
#radio.setFrequency(ft847.MAIN_VFO, 1123456.123)
radio.setFrequency(ft847.MAIN_VFO, 436000000.123)
#radio.setMainVfoOperatingMode('FM(N)')
#radio.setMainVfoCtcssDcsMode("CTCSS ENC ON")
#radio.setMainVfoCtcssFrequency("114.8")
#radio.setMainVfoDcsCode(754)
radio.setRepeaterShift('-')
radio.setRepeaterOffset(650000)
#Below two might not work if sattellite mode is not enabled
#print radio.getSatRxVfoStatus()
#print radio.getSatTxVfoStatus()
radio.disconnect()

