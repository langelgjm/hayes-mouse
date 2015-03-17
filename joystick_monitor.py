#!/usr/bin/python

import sys
import serial
from pymouse import PyMouse

def decodeJoystick(joyString):
	joyLong = long(joyString, 16)
	xPos = joyLong & 0x3F
	yPos = (joyLong >> 6) & 0x3F
	but1 = (joyLong >> 12) & 0x1
	but2 = (joyLong >> 13) & 0x1
	time = joyLong >> 14
	# Actually mixed up the axes in the encoded data, so swap here
	return {"xPos":yPos, "yPos":xPos, "but1":but1, "but2":but2, "time":time}

def main():
	try:
		m = PyMouse()
		xScr, yScr = m.screen_size()
		xMult = xScr / 63
		yMult = yScr / 63
		m.move(0,0)
		ser = serial.Serial('/dev/ttyACM0', 9600)
		while True:
			if ser.inWaiting():
				l = ser.readline()
				ls = l.split()
				# Sometimes we miss a newline and only get a CR
				for l in ls:
					l.strip()
					if l == '':
						continue
					d = decodeJoystick(l)
					output = "xpos = {0:2d}, ypos={1:2d}, but1 = {2}, but2 = {3}, time = {4:6d}, raw = {5:10s}".format(d["xPos"], d["yPos"], d["but1"], d["but2"], d["time"], l)
					print output
					# Lazy but good enough for proof of concept
					xMove = d["xPos"]*xMult
					yMove = yScr - d["yPos"]*yMult
					m.move(xMove, yMove)
					if d["but1"]==1:
						m.click(xMove, yMove, 1)
	except serial.SerialException:
		main()
	except KeyboardInterrupt:
		ser.close()
		sys.exit()

if __name__ == "__main__":
    main()
