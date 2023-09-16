/*
  Multiple Serial test

  Receives from the main serial port, sends to the others.
  Receives from serial port 1, sends to the main serial (Serial 0).

  This example works only with boards with more than one serial like Arduino Mega, Due, Zero etc.

  The circuit:
  - any serial device attached to Serial port 1
  - Serial Monitor open on Serial port 0

  created 30 Dec 2008
  modified 20 May 2012
  by Tom Igoe & Jed Roach
  modified 27 Nov 2015
  by Arturo Guadalupi

  This example code is in the public domain.
*/
#include <SoftwareSerial.h>
SoftwareSerial mySerial(0, 1); // RX, TX

void setup() {
  // initialize both serial ports:
  Serial.begin(38400);
  mySerial.begin(38400);
  Serial.print("Baudrate:38400");
}

void loop() {
  // read from log UART, send to port 1:
  if (mySerial.available()) {
    int inByte = mySerial.read();
    Serial.write(inByte);
  }

  // read from port 1, send to log UART:
  if (Serial.available()) {
    int inByte = Serial.read();
    mySerial.write(inByte);
  }
}
