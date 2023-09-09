//TempAndHumidity, Sensing by Pin6
#include "DHT.h"
#define DHTPIN 5
#define DHTTYPE DHT11   // DHT 11
#include <SoftwareSerial.h>

SoftwareSerial mySerial(0, 1); // RX, TX

DHT dht(DHTPIN, DHTTYPE);// Initialize DHT sensor.
void setup()
{
  Serial.begin(115200);
  mySerial.begin(9600);
  dht.begin();
  Serial.println("Temp and Humidity Test");

}
void loop()
{
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t) ) {
    Serial.println("Failed to read from DHT sensor!");
    //return;
  }
  else {
    Serial.print(h);
    Serial.print(",");
    Serial.println(t);
    mySerial.print('H');
    mySerial.print(',');
    mySerial.print(h,1); //顯示濕度至小數點以下1位；
    mySerial.print(',');
    mySerial.print(t,1); //顯示溫度至小數點以下1位；
    mySerial.println(',');

  }
  delay(3000);
}
