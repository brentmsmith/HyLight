# HyLight
## A collection of software that can be used to control the iLuminator and HyLight boards

### Arduino code for transmitter/receiver HyLight-Arduino interface boards:

Any form of serial communication can be used to send data to the a transmitter. The recommended method is PySerial. If PySerial is not installed, install using: `$ sudo pip install pyserial`. The baud must be set to 9600 and the data to be transmitted must be in the form of a string with 11 digits, e.g. "1 100 500 300 350 0 250 80 600 250 0". The string must also be encoded into byte data. This string tells the transmitter to send 10 PWM values to a specific HyLighter, in this case HyLighter Receiver #02 will set LED 1, 2, 3, 4, 5, 7, 8, and 9 to a duty cycle of 100, 500, 300, 350, 250, 80, 600, and 250, respectively. LEDs 5 and 10 are not turned on, i.e. the duty cycle is set to 0. The first digit indicates the HyLight number, so a value of 0 corresponds to HyLight Receiver #1, a value of 1 to HyLight Receiver #2, and so on. The next ten digits indicates the duty cycle of the 10 HyLight LEDs, with 4096 being the absolute max. The HyLight will never reach the max power of one LED, and will continuously turn off if the duty cycle is set to max. **Always stay below 15% of any LEDs max duty cycle to avoid damaging the HyLighter LED boards.**  


Sending the 10 HyLight LED duty-cycles using PySerial:  
```
import serial 
ard = serial.Serial('/dev/cu.usbmodem1481',9600) 
ard.write('0 40 0 0 0 0 0 0 0 0 0'.encode()) 
```

These 3 lines tell _HyLighter Receiver #01_ (indicated by the first digit of `0` in the `ard.write` string) to turn on only the 1st LED to 0.98% of the max duty cycle (40/4096=0.98%).   
The first line imports PySerial  
The second line creates a PySerial object, where the first argument is the serial port location, and the second argument is the baud rate (must be set to 9600)  
The third line uses the PySerial `write` function to send a string to the transmitter arduino via USB serial communication. This string then gets parsed into the integers it contains by the transmitter arduino, and 10 of those integers are transmitted to a receiver arduino. The first number in the string is the receiver number. This number is used to access a receiver address that is stored in the transmitter arduino memory. The subsequent 10 numbers are the LED duty-cycles. These values have a max of 4096, **but should never exceed 15% of this number (<=614)**. The `.encode()` method casts the string into byte data so the transmitter arduino will understand the data.  

The string to be sent to the transmitter via PySerial should be formatted as:  

- _0th_: The receiver number. This number accesses the RF address stored on the transmitter arduino and opens a communication pipe with the receiver arduino that has the specified address stored on it. There are 8 addresses in the transmitter arduino code, and each receiver is flashed with a unique address out of those 8. A receiver number of 0 in the string will open a communication pipe with the receiver labeled _"SciHub HyLighter Receiver #01"_, a receiver number of 1 will open a pipe with the receiver labeled _"SciHub HyLighter Receiver #02"_, and so on...   
- _1st_: The duty cycle of the 1st LED  
- _2nd_: The duty cycle of the 2nd LED  
- .  
- .  
- _10th_: The duty cycle of the 10th LED  
