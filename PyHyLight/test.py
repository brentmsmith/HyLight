# -*- coding: utf-8 -*-
'''

Run this code to test the PyHyLight library, the NRF-Arduino
transmitter/receiver modules, and the HyLight boards themselves

'''
# Required imports
from pyhylight import *
import numpy as np
import time

# Open ard serial port
tran = serial.Serial('/dev/ttyACM0',9600) # Change this to your actual transmitter arduino serial port path
notes = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
off = np.zeros(10) # Array of zeros to turn off HyLights

hylighter_ix = range(0,8)
serial_wait = .05 #wait time between each send in sec

# Cycle through Mary's colors, all the same color
for note in notes:
    [(time.sleep(serial_wait),send(tran,ix,hylrgb(maryrgb[note]),power=10)) for ix in hylighter_ix]
    
    time.sleep(1.5)
    
    [(time.sleep(serial_wait), send(tran,ix, off)) for ix in hylighter_ix]

# Cycle through Mary's colors, alternating
i,j,k,l,m,n = 0,1,2,3,4,5
for note in notes*2:
	send(tran,0,hylrgb(maryrgb[notes[i]]),power=10)
	send(tran,1,hylrgb(maryrgb[notes[j]]),power=10)
	send(tran,2,hylrgb(maryrgb[notes[k]]),power=10)
	send(tran,3,hylrgb(maryrgb[notes[l]]),power=10)
	send(tran,4,hylrgb(maryrgb[notes[m]]),power=10)
	send(tran,5,hylrgb(maryrgb[notes[n]]),power=10)
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


[(time.sleep(serial_wait), send(tran,ix, off)) for ix in hylighter_ix]

# Cycle through Mary's colors faster
for note in notes*3:
	send(tran,0,hylrgb(maryrgb[notes[i]]),power=10)
	send(tran,1,hylrgb(maryrgb[notes[j]]),power=10)
	send(tran,2,hylrgb(maryrgb[notes[k]]),power=10)
	send(tran,3,hylrgb(maryrgb[notes[l]]),power=10)
	send(tran,4,hylrgb(maryrgb[notes[m]]),power=10)
	send(tran,5,hylrgb(maryrgb[notes[n]]),power=10)
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

[(time.sleep(serial_wait), send(tran,ix, off)) for ix in hylighter_ix]
