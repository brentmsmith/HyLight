#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h> // See https://maniacbug.github.io/RF24/ for more 

#define CE_PIN   9
#define CSN_PIN 10
#define SERIAL_RX_BUFFER_SIZE 256
#define SERIAL_TX_BUFFER_SIZE 256

RF24 radio(CE_PIN, CSN_PIN); // Create a NRF24l01 object using the specified CE/CSN pins

/*
 * The 8 receiver addresses are listed below, with each receiver flashed to one from the list
 */
const byte slaveAddress[8][5] = {{'R','x','L','A','A'},{'R','x','A','Q','B'},{'B','t','A','q','B'},{'I','x','E','b','B'},{'P','c','A','V','S'},{'A','h','U','p','k'},{'R','x','h','U','L'},{'P','o','4','G','J'}};

int rec=10; // Instantiate the receiver number to 10

void setup() {
    Serial.begin(9600);  // Begin USB serial communication with a baud rate of 9600
    radio.begin();       // Initiate the NRF24l01 module
    radio.setPALevel(RF24_PA_MAX); //Set Power Amplifier level to max
    radio.setDataRate( RF24_2MBPS ); //Set transmission rate to 2 MBPS
    radio.setRetries(0,0); // delay, count, off for transmission speed
    radio.stopListening(); // Go into transmission mode only
    radio.setPayloadSize(255); // 255 bytes
    radio.setAutoAck(false); // Auto acknowledge turned off for faster communication, but can be turned on if noise becomes an issue.
    Serial.setTimeout(11);   // Time out serial transmission after 11 ms if nothing received  
}

void loop() {
  int data[10]; // Initializing the duty-cycles of the 10 LEDs
  /*
   * If serial data is received, read in the 11 digit string and parse out
   * the string into respective integers. The first integer is the HyLight-
   * Arduino interface board, the next 10 are the duty cycles of the 10 LEDs
   */
  if (Serial.available() > 0) { 
    rec = Serial.parseInt();
    data[0] = Serial.parseInt();
    data[1] = Serial.parseInt();
    data[2] = Serial.parseInt();
    data[3] = Serial.parseInt();
    data[4] = Serial.parseInt();
    data[5] = Serial.parseInt();
    data[6] = Serial.parseInt();
    data[7] = Serial.parseInt();
    data[8] = Serial.parseInt();
    data[9] = Serial.parseInt();
    radio.openWritingPipe(slaveAddress[rec]); // Open up a pipe to the designated HyLighter
    radio.write( &data, sizeof(data) );       // Transmit the 10 integer array to the designated HyLighter board
  }

}
