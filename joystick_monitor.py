#!/usr/bin/python

import sys
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

def decodeJoystick(joyString):
	joyLong = long(joyString, 16)
	xPos = joyLong & 0x3F
	yPos = (joyLong >> 6) & 0x3F
	but1 = (joyLong >> 12) & 0x1
	but2 = (joyLong >> 13) & 0x1
	time = joyLong >> 14
	return (xPos, yPos, but1, but2, time)

def main():
	try:
		while True:
			if ser.inWaiting():
				l = ser.readline()
				ls = l.split()
				# Sometimes we miss a newline and only get a CR
				for l in ls:
					l.strip()
					if l == '':
						continue
					s = decodeJoystick(l)
					output = "xpos = {0:2d}, ypos={1:2d}, but1 = {2}, but2 = {3}, time = {4:6d}, raw = {5:10s}".format(s[0], s[1], s[2], s[3], s[4], l)
					print output
	except serial.SerialException:
		main()
	except KeyboardInterrupt:
		ser.close()
		sys.exit()

if __name__ == "__main__":
    main()
