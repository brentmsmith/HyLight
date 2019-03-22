# HyLight
## A collection of software that can be used to control the iLuminator and HyLight boards

### Arduino code for transmitter/receiver HyLight-Arduino interface boards:

Any form of serial communication can be used to send data to the a transmitter. The recommended method is PySerial. The baud must be set to 9600 and the data must be a string with 11 digits, e.g. "1 100 500 300 900 0 250 80 600 700 0". This string tells the transmitter to send 10 PWM values to a specific HyLight, in this case HyLight #2 will set LED 1, 2, 3, 4, 5, 7, 8, and 9 to a duty cycle of 100, 500, 300, 900, 250, 80, 600, and 700, respectively. LEDs 5 and 10 are not turned on, i.e. the duty cycle is set to 0. The first digit indicates the HyLight number, so a value of 0 corresponds to HyLight #1, a value of 1 to HyLight #2, and so on. The next ten digits indicates the duty cycle of the 10 HyLight LEDs, with 4096 being the absolute max. The HyLight will never reach the max power of one LED, and will continuously turn off if the duty cycle is set to max. Always stay below 15% of any LEDs max duty cycle to avoid damaging the HyLighter boards. 


Sending the 10 HyLight LED duty-cycles using PySerial:
```
import serial 
ard = serial.Serial('/dev/cu.usbmodem1481',9600) 
ard.write('0 40 0 0 0 0 0 0 0 0 0'.encode()) 
```

If PySerial is not installed, install using: $ sudo pip install pyserial
The first line imports PySerial
The second line creates a PySerial object, where the first argument is the serial port location, and the second argument is the baud rate (must be set to 9600)
The third line uses the write function to send a string to the transmitter arduino. This string then gets parsed into integers in the transmitter arduino, and 10 of those integers are transmitted to a receiver arduino. The first number in the string is the receiver number. This number is used to access a receiver address that is stored in the transmitter arduino memory. The subsequent 10 numbers are the LED duty-cycles. These values have a max of 4096, **but should never exceed 15% of this number (<=614)**. 

The string to be sent to the transmitter via PySerial should be formatted as:

0th: The receiver number. This number accesses the address stored on the transmitter and opens a communication pipe with the receiver of the same address. There are 8 addresses in the transmitter arduino code, and each receiver is flashed with a unique address out of those 8. 

1st: The duty cycle of the 1st LED

2nd: The duty cycle or the 2nd LED

.

.

etc.



