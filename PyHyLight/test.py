'''

Run this code to test the PyHyLight library, the NRF-Arduino 
transmitter/receiver modules, and the HyLight boards themselves

'''
# Required imports
from pyhylight import *
import numpy as np
import time

# Open ard serial port
ard.port = '/dev/tty.usbmodem1411' # Change this to your actual transmitter arduino serial port path
ard.open()
notes = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
off = np.zeros(10) # Array of zeros to turn off HyLights

# Cycle through Mary's colors, all the same color
for note in notes:
	send(0,hylrgb(maryrgb[note]),power=10)
	send(1,hylrgb(maryrgb[note]),power=10)
	send(2,hylrgb(maryrgb[note]),power=10)
	send(3,hylrgb(maryrgb[note]),power=10)
	send(4,hylrgb(maryrgb[note]),power=10)
	send(5,hylrgb(maryrgb[note]),power=10)
	time.sleep(1.5)
	send(0,off)
	send(1,off)
	send(2,off)
	send(3,off)
	send(4,off)
	send(5,off)

# Cycle through Mary's colors, alternating
i,j,k,l,m,n = 0,1,2,3,4,5
for note in notes*2:
	send(0,hylrgb(maryrgb[notes[i]]),power=10)
	send(1,hylrgb(maryrgb[notes[j]]),power=10)
	send(2,hylrgb(maryrgb[notes[k]]),power=10)
	send(3,hylrgb(maryrgb[notes[l]]),power=10)
	send(4,hylrgb(maryrgb[notes[m]]),power=10)
	send(5,hylrgb(maryrgb[notes[n]]),power=10)
	i,j,k,l,m,n=i+1,j+1,k+1,l+1,m+1,n+1
	if i>11:
		i=0
	if j>11:
		j=0
	if k>11:
		k=0
	if l>11:
		l=0
	if m>11:
		m=0
	if n>11:
		n=0
	time.sleep(1)

send(0,off)
send(1,off)
send(2,off)
send(3,off)
send(4,off)
send(5,off)

# Cycle through Mary's colors faster
for note in notes*3:
	send(0,hylrgb(maryrgb[notes[i]]),power=10)
	send(1,hylrgb(maryrgb[notes[j]]),power=10)
	send(2,hylrgb(maryrgb[notes[k]]),power=10)
	send(3,hylrgb(maryrgb[notes[l]]),power=10)
	send(4,hylrgb(maryrgb[notes[m]]),power=10)
	send(5,hylrgb(maryrgb[notes[n]]),power=10)
	i,j,k,l,m,n=i+1,j+1,k+1,l+1,m+1,n+1
	if i>11:
		i=0
	if j>11:
		j=0
	if k>11:
		k=0
	if l>11:
		l=0
	if m>11:
		m=0
	if n>11:
		n=0
	time.sleep(.3)

send(0,off)
send(1,off)
send(2,off)
send(3,off)
send(4,off)
send(5,off)
