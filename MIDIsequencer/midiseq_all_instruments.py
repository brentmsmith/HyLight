from __future__ import division
from pyhylight import *
import serial,time,mido,sys
import numpy as np

tran = serial.Serial('/dev/ttyACM0',9600,write_timeout=0)
tran2 = serial.Serial('/dev/ttyACM1',9600,write_timeout=0)
tran3 = serial.Serial('/dev/ttyACM2',9600,write_timeout=0)

if len(sys.argv)!=2:
    print('Please add a midi file to the execution command, e.g.:\npython midiseq.py song.mid')
    sys.exit()
else:
    song = mido.MidiFile(sys.argv[1])

off = np.zeros(10) # For sending an off command to the HyLighter
send(tran,0,off)
time.sleep(1)
tran.flushInput()
send(tran,0,off)
'''
The outport can be commented if you are not listening to the midi
notes on your computer. To open a virtual midi port on linux,
first install TiMidity with apt-get, then run 'aconnect -o' then 
'timidity -iA'.
For OSX, open a virtual midi port with garageband from the Audio 
MIDI Setup app. Choose Window -> Show MIDI Studio. Double-click
on IAC Drive, and check if Device is online.
'''
outport = mido.open_output('TiMidity port 0')
#outport = mido.open_output('New Port',virtual=True,client_name='My Client')
#outport = mido.open_output('virtual',virtual=True)
outport.reset()
time.sleep(.1)

print([track.name for track in song.tracks]) # All the Tracks
pianotrack = np.asarray([(track.name=='Cassiopeia' or track.name=='Finale') for track in song.tracks]) # The piano tracks for Cassiopeia and Finale
numtrax = np.arange(len(song.tracks)) # A list of track channels
piano = int(numtrax[pianotrack]) # The channel of the piano

chanlevels = np.zeros((len(song.tracks),10)) #Create array to keep track of colors for adding together RGB values

input('Press Enter when ready')

for msg in song.play():
	if msg.is_meta:
		continue
	outport.send(msg) # Can be removed if you're not sending sounds to a virtual midi port
	if (msg.type=='note_on'):
		chanlevels[msg.channel]+=hylrgb(maryrgb[num2note(msg.note)]) # Add polyphonic RGB values together, usually looks white 
		'''
		Have only one transmitter handle 2 channels at a time.
		Improves speed by allowing one buffer to be cleared 
		between 2 channels per transmitter. 
		'''
		if msg.channel==0 or msg.channel==1:
			print(msg.channel,'on',num2note(msg.note))
			send(tran,msg.channel,chanlevels[msg.channel],power=100)
			tran.flushInput()
		elif msg.channel==2 or msg.channel==3:
			print(msg.channel,'on',num2note(msg.note))
			send(tran2,msg.channel,chanlevels[msg.channel],power=100)
			tran2.flushOutput()
		elif msg.channel==4 or msg.channel==5:
			print(msg.channel,'on',num2note(msg.note))
			send(tran3,msg.channel,chanlevels[msg.channel],power=100)
			tran3.flushOutput()
	if (msg.type=='note_off'):
		chanlevels[msg.channel]-=hylrgb(maryrgb[num2note(msg.note)]) # Now subtract those RGB values from the color
		if msg.channel==0 or msg.channel==1:
			print(msg.channel,'off',num2note(msg.note))
			send(tran,msg.channel,chanlevels[msg.channel],power=100)
			tran.flushInput()
		elif msg.channel==2 or msg.channel==3:
			print(msg.channel,'off',num2note(msg.note))
			send(tran2,msg.channel,chanlevels[msg.channel],power=100)
			tran2.flushOutput()
		elif msg.channel==4 or msg.channel==5:
			print(msg.channel,'off',num2note(msg.note))
			send(tran3,msg.channel,chanlevels[msg.channel],power=100)
			tran3.flushOutput()


print('Kill this loop with ctrl+c')  
i=0
ledz=np.zeros(10)
while True:
	i+=0.1
	for j in range(10):
		ledz[j]=np.sin(2*np.pi*j/10+i)/2+1/2
	send(tran1,0,ledz,power=100)
	tran.flushInput()
	send(tran2,2,ledz,power=100)
	tran2.flushInput()
	send(tran3,4,ledz,power=100)
	tran3.flushInput()
	