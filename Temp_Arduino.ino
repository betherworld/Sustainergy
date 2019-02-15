
void setup(){
  Serial.begin(9600);
}


void loop(){
  float voltage, degreesC;
  float reading = (float)analogRead(0);
  voltage = reading *5/1024;
  degreesC = (voltage - 0.5) * 100.0;
  Serial.print("reading: ");
  Serial.print(reading);
  Serial.print(" voltage: ");
  Serial.print(voltage);
  Serial.print("  deg C: ");
  Serial.println(degreesC);   
  delay(1000);
}
