/**
 * Copyright (c) 2009 Andrew Rapp. All rights reserved.
 *
 * This file is part of XBee-Arduino.
 *
 * XBee-Arduino is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * XBee-Arduino is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with XBee-Arduino.  If not, see <http://www.gnu.org/licenses/>.
 */
/*
 * 我的修改說明：
 * 1.我將傳送的資料從兩個Byte的Analog Input改為隨機溫溼度數值，並用逗號隔開
 * 2.我的修改在GPL許可下發布。
 */

#include <XBee.h>
#include <SoftwareSerial.h>
#include "DHT.h"
#define DHTPIN 7     // what digital pin we're connected to
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);

#if defined(BOARD_RTL8195A)
SoftwareSerial mySerial(0, 1); // RX, TX
#elif defined(BOARD_RTL8710)
SoftwareSerial mySerial(17, 5); // RX, TX
#else
SoftwareSerial mySerial(0, 1); // RX, TX
#endif
/*
This example is for Series 2 XBee
 Modified from "Series2-Tx" Example of XBee-Arduino library
 Sends a ZB TX request with the value of temperature and humidity value acquired from DHT 11 sensor and checks the status response for success
*/

// create the XBee object
XBee xbee = XBee();

uint8_t payload[10];
char strBuffer[10];
int humid,temp;

// SH + SL Address of receiving XBee, (0,0) for coordinator
XBeeAddress64 addr64 = XBeeAddress64(0, 0);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

int pin5 = 0;

int statusLed = 13;
int errorLed = 13;

void flashLed(int pin, int times, int wait) {

  for (int i = 0; i < times; i++) {
    digitalWrite(pin, HIGH);
    delay(wait);
    digitalWrite(pin, LOW);

    if (i + 1 < times) {
      delay(wait);
    }
  }
}

void setup() {
  pinMode(statusLed, OUTPUT);
  pinMode(errorLed, OUTPUT);

  Serial.begin(9600);
  mySerial.begin(9600);
  xbee.setSerial(mySerial);
  //初始化DHT11感知器
  dht.begin();
}

void loop() {   
  // break down 10-bit reading into two bytes and place in payload
  //  pin5 = analogRead(5);
  // Random產生溫溼度數值
  //  humid=random(50,81);
  //  temp=random(10,41);
  // 從DHT11感知器取得溫溼度數值
      delay(1000);
      float h=dht.readHumidity();
      float t=dht.readTemperature();
      if (isnan(h) || isnan(t)) {
        Serial.println("Failed to read from DHT sensor!");
        return;
      }
      humid=(int)h;
      temp=(int)t;
  sprintf(strBuffer, "%02d,%02d,", humid, temp);
  Serial.print("strBuffer:");
  Serial.print(strBuffer);
  Serial.print("\r\n");

  for(int i=0;i<strlen(strBuffer);i++){
    payload[i]=(uint8_t)strBuffer[i];
  }

  xbee.send(zbTx);

  // flash TX indicator
  flashLed(statusLed, 1, 100);

  // after sending a tx request, we expect a status response
  // wait up to half second for the status response
  if (xbee.readPacket(500)) {
    // got a response!

    // should be a znet tx status            	
    if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
      xbee.getResponse().getZBTxStatusResponse(txStatus);

      // get the delivery status, the fifth byte
      if (txStatus.getDeliveryStatus() == SUCCESS) {
        // success.  time to celebrate
        flashLed(statusLed, 5, 50);
      } else {
        // the remote XBee did not receive our packet. is it powered on?
        flashLed(errorLed, 3, 500);
      }
    }
  } else if (xbee.getResponse().isError()) {
    //nss.print("Error reading packet.  Error code: ");  
    //nss.println(xbee.getResponse().getErrorCode());
  } else {
    // local XBee did not provide a timely TX Status Response -- should not happen
    flashLed(errorLed, 2, 50);
  }

  delay(1000);
}
