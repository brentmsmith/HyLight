# MIDI sequencer

### These python scripts will send Mary's color-note synesthesia RGB colors to the HyLighters using the included .mid files

There are 2 versions of the script that can be run during the performance. One will only use Mary's piano notes in the midi files and send those colors to the Hylighters (midiseq_piano_only.py), and the other will be able to use all of the instruments in the midi files and send colors to separate hylighter per midi channel (midiseq_all_instruments.py). Which one to use is users choice. Using only the piano may run into problems with the serial buffer, unless the Receiver Arduinos are flashed to have the same address. Cassiopiea only has a few piano notes in the song. I recommend trying to use `midiseq_all_instruments.py` with 3 transmitters during tests and rehearsals for this reason. 

- With using only the piano to send the colors to the 6 receivers, the code will still have to iterate over 6 send commands with the same delay needed for the buffer (~0.04 seconds). Otherwise, the Receiver Arduinos will have to be flashed so they all have same address, which will have to be the first one off the list in the [arduino code](https://github.com/MachineAlfr/HyLight/blob/master/ArduinoNRF/HyLight_NRF_receiver.ino) (that address is: `{'R','x','L','A','A'}`) . Sending one transmission intended for 6 receivers has not been tested. 

- The piano playing in the Cassiopeia midi file is pretty sparse. The Hylighters would be off for a lot of the song. 

- Using 3 transmitters and running the midiseq_all_instruments.py code as is after any tweaking needed should be relatively straight forward. Clearing the buffer on 3 different serial lines should be faster than clearing one buffer over and over. PySerial supports threading as well, so if clearing the buffer is still slowing things down, buffer clearing on different transmitters can be managed by a separate thread in the background. There didn't seem to be a need for this while testing though. 

Other notes:
- For chords, I only had time to implement an additive color scheme for the RGB note colors. Ideally it would be the root note of the chord that is sent to the Hylighter, but keeping track of the notes in a chord per channel is a problem that will take more time to solve. Therefore chords looks close to white. I'm open to collaboration on this problem if there's time to solve it.

- The code relies on the pyhylight library (included in this repo), serial, numpy, mido, and rtmidi. You may have to install rtmidi with: `$ sudo pip3 install python-rtmidi`

- For testing or rehearsing, you can open a virtual midi port on the computer to play the notes on it's speakers as the code simultaneously send colors to the hylighter. There are different ways for doing this for different OS's. For linux, you need to install TiMidity using apt-get, then run `$ aconnect -o` then `$ timidity -iA`. For OSX, open Garageband, then open the "Audio MIDI Setup" app in Applications->Utilities. From the menu select Window->Show MIDI Studio, then double click on IAC Drive. Make sure Device is online is checked.

- Finale seems to hang at the end of the song, and I'm not sure why. The code can be killed with ctrl-c if that persists. I would have a separate tab opened in the terminal to send an off command to the hylighters, e.g. `send(tran,0,np.zeros(10))`

- The code ends by cycling through the Hylighters variety colors after the midi sequence. This can be killed with ctrl-c again when it's time to stop. You can run `$ python killhyl.py` to turn off all the hylighters as needed.

#### To execute the code
Just type `$ python3 midiseq_all_instruments.py 1_Cassiopeia_[UPADTEDfor2019].mid` in your terminal. You will be prompted to hit the enter key to begin the sequence. 
