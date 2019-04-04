from __future__ import division
from pyhylight import *
import serial,time,mido,sys
import numpy as np

tran = serial.Serial('/dev/ttyACM0',9600,write_timeout=0)

if len(sys.argv)!=2:
    print('Please add a midi file to the execution command, e.g.:\npython midiseq.py song.mid')
    sys.exit()
else:
    song = mido.MidiFile(sys.argv[1])

off = np.zeros(10)
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

chanlevels = np.zeros((len(song.tracks),10)) # Create array to keep track of colors for adding together RGB values

input('Press Enter when ready')

for msg in song.play():
	if msg.is_meta:
		if msg.type=='end_of_track':
			break
		continue
	outport.send(msg)
	if (msg.type=='note_on'):
		chanlevels[msg.channel]+=hylrgb(maryrgb[num2note(msg.note)])
		if msg.channel==piano:
			print(msg.channel,'on',num2note(msg.note))
			send(tran,0,chanlevels[piano])
			tran.flushInput()
	if (msg.type=='note_off'):
		chanlevels[msg.channel]-=hylrgb(maryrgb[num2note(msg.note)])
		if msg.channel==piano:
			print(msg.channel,'off',num2note(msg.note))
			send(tran,0,chanlevels[piano])
			tran.flushInput()


print('Kill this loop with ctrl+c')   
i=0
ledz=np.zeros(10)
while True:
	i+=0.1
	for j in range(10):
		ledz[j]=np.sin(2*np.pi*j/10+i)/2+1/2
	send(tran,0,ledz,power=100)
	time.sleep(0.04)
	send(tran,2,ledz,power=100)
	time.sleep(0.04)
	send(tran,4,ledz,power=100)
	time.sleep(0.04)
	