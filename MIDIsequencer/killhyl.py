from __future__ import division
from pyhylight import *
import numpy as np

tran = serial.Serial('/dev/ttyACM0',9600,write_timeout=0)
off = np.zeros(10)

for i in range(6):
	send(tran,i,off)
	tran.flushInput()