# PyHyLight

### This module contains various functions for sending colors via serial commands to a transmitter Arduino to be sent to a receiver Arduino. The transmitted data is a string of 10 LED dutycycles, which are then set to each HyLighter LED. 

To send an RGB color of (187, 70, 192) to the HyLighter board, the following python code can be run:
```
from pyhylight import send, hylrgb

tran = serial.Serial('/dev/cu.usbmodem1',9600) # The path of your transmitter Arduino port will be different. Try finding it using the Arduino IDE
send(tran,0,hylrgb((187, 70, 192)))     # Sends the RGB color (187, 70, 192) to the transmitter to be displayed on a HyLight
```

To send an RGB color that corresponds to Mary's note-color synesthesia, you can send an A flat with:
```
from pyhylight import *

tran2 = serial.Serial('/dev/tty.usbmodem1411',9600)
send(tran2,0,hylrgb(maryrgb['Ab']))      # Mary's synesthesia RGB colors are preloaded in a dictionary called maryrgb, and can be referenced by note name
```
