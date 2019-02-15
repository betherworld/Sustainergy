void setup() {
  //Init Communication
  Serial.begin(9600);
}

void loop(){
  //Read Voltage
  float reading = (float)analogRead(0);
  float voltage = reading *5/1024;
  //Compute Temperature
  float degreesC = (voltage - 0.5) * 100.0;
  //Filter Errors
  if(degreesC > 10){
    //Send Temperature
    Serial.println(degreesC);
    //Wait a second
    delay(1000); 
  }
}
