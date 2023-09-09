# 1 "d:\\project\\ameba-arduino-samples\\TempAndHumidity\\TempAndHumidity.ino"
//TempAndHumidity, Sensing by Pin6
# 3 "d:\\project\\ameba-arduino-samples\\TempAndHumidity\\TempAndHumidity.ino" 2



DHT dht(8, 11 /* DHT 11*/);// Initialize DHT sensor.
void setup()
{
  Serial.begin(115200);
  dht.begin();
  Serial.println("Temp and Humidity Test");

}
void loop()
{
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if ((((sizeof(h) == sizeof(float)) ? __fpclassifyf(h) : __fpclassifyd(h)) == 0) || (((sizeof(t) == sizeof(float)) ? __fpclassifyf(t) : __fpclassifyd(t)) == 0) ) {
    Serial.println("Failed to read from DHT sensor!");
    //return;
  }
  else {
    Serial.print('H');
    Serial.print(',');
    Serial.print(h,1); //顯示濕度至小數點以下1位；
    Serial.print(',');
    Serial.print(t,1); //顯示溫度至小數點以下1位；
    Serial.println(',');

  }
  delay(3000);
}
