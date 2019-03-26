# PyHyLight

### This module contains various functions for sending colors via serial commands to a transmitter Arduino to be sent to a receiver Arduino. The transmitted data is a string of 10 LED dutycycles, which are then set to each HyLighter LED. 

To send an RGB color of (187, 70, 192) to the HyLighter board, the following python code can be run:
```
from pyhylight import send, 

ard.port = '/dev/tty.usbmodem1411'
ard.open()
send(0,hylrgb((187, 70, 192)))
```

To send an RGB color that corresponds to Mary's note-color synesthesia, you can send an A natural with:
```
from pyhylight import *

ard.port = '/dev/tty.usbmodem1411'
ard.open()
send(0,hylrgb(maryrgb['A']))
```
