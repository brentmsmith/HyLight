#include <SPI.h>
#include <nRF24L01.h> //https://github.com/nRF24/RF24
#include <RF24.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h> //https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library

#define CE_PIN  9
#define CSN_PIN 10

const byte thisSlaveAddress[5] = {'R','x','L','A','A'};
/* Other slave addresses are:
 * {'R','x','L','A','A'}
 * {'R','x','A','Q','B'}
 * {'B','t','A','q','B'}
 * {'I','x','E','b','B'}
 * {'P','c','A','V','S'}
 * {'A','h','U','p','k'}
 * {'R','x','h','U','L'}
 */

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(); // Create a i2c pwm object to control the PCA9685 drivers on the HyLighter interface boards
RF24 radio(CE_PIN, CSN_PIN); 

int dataReceived[10]; // The 10 integers sent by the transmitter

void setup() {
    Serial.begin(9600);                         // Begin serial communication if needed
    radio.begin();                              // Initialize the NRF24l01 module
    radio.setDataRate( RF24_2MBPS );            // Set the data rate to 2 MBPS
    radio.openReadingPipe(1, thisSlaveAddress); // Begin listening for broadcasts of the specified receiver address
    radio.setPayloadSize(255);                  // Set the packet size to 255 bytes
    radio.startListening();                     // Start being a receiver  
    radio.setAutoAck(false);                    // Turn off auto-acknowledge to maximize comm speed
    pwm.begin();                                // Initialize the PCA9685 PWM driver
    pwm.setPWMFreq(1600);                       // Set the frequency to 1.6 kHz
    Wire.setClock(400000);                      // Set I2C clock frequency to 400 kHz
}

void loop() {
  /* If the NRF24l01 object receives a packet, the packet is
   * iterated over and the the LED PWM values are set to the 
   * elements of the 10 element array packet
   */
  if(radio.available()){ 
    radio.read( &dataReceived, sizeof(dataReceived) );
    for(int i = 0; i < 10; i++){
      pwm.setPWM((uint8_t) i, 0, (uint16_t) dataReceived[i]);
    }
  }
}
