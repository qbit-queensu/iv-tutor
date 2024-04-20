const int voutPin0 = A0;
const int voutPin1 = A1;

void setup() {
  Serial.begin(9600);
  delay(2);
  pinMode(voutPin0, INPUT);
  pinMode(voutPin1, INPUT);

  delay(2000);
  Serial.println("Setup Complete");
}

// the loop function runs over and over again forever
void loop() {
  // Measure needle voltage
  float needleVoltage = analogRead(voutPin0)/1024.0*5.0;
  Serial.print("Analog 0: ");
  Serial.println(analogRead(voutPin0)/1024.0*5.0);

  // Measure posterior wall voltage
  float pwVoltage = analogRead(voutPin1)/1024.0*5.0;
  Serial.print("Analog 1: ");
  Serial.println(analogRead(voutPin1)/1024.0*5.0);
  
  if (needleVoltage >= 0.5){
    Serial.println("Successful Needle Insertion");
  }else if (pwVoltage >= 0.5){
    Serial.print("Needle has punctured the vein's posterior wall");
  }else{
    Serial.println("Needle is is not in vein!");
  }
  
  delay(1000);                          // wait for a second
}
