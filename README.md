# HyLight
A collection of software that can be used to control the iLuminator and HyLight boards

Arduino code for transmitter/receiver HyLight-Arduino interface boards:

Any form of serial communication can be used to send data to the a transmitter. The recommended method is PySerial. The baud must be set to 9600 and the data must be a string with 11 digits, e.g. "1 100 500 300 900 0 250 80 600 700 0". This string tells the transmitter to send 10 PWM values to a specific HyLight, in this case HyLight #2 will set LED 1, 2, 3, 4, 5, 7, 8, and 9 to a duty cycle of 100, 500, 300, 900, 250, 80, 600, and 700, respectively. LEDs 5 and 10 are not turned on, i.e. the duty cycle is set to 0. The first digit indicates the HyLight number, so a value of 0 corresponds to HyLight #1, a value of 1 to HyLight #2, and so on. The next ten digits indicates the duty cycle of the 10 HyLight LEDs, with 4096 being the absolute max. The HyLight will never reach the max power of one LED, and will continuously turn off if the duty cycle is set to max. Always stay below 50% of any LEDs max duty cycle to avoid damaging the HyLighter boards. 
