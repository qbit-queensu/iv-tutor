// Input Pins
const int voutNeedle = A0;   // Pin A0 is connected to the needle
const int voutPostWall = A1; // Pin A1 is connected to the posterior wall
#define START 4              // Pin 8 Measures the state of the start switch

// Output Pins
#define STATUS 11 // Pin 11 controls the ON/OFF relay
#define RELAY1 12 // Pin 12 controls the GROUND relay 
#define RELAY2 13 // Pin 13 controls the 6V relay


// Global variables
long randPosition = 0;
bool enable_circuit = 1;
bool prevSwitchState = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(200);
  
  pinMode(voutNeedle, INPUT);
  pinMode(voutPostWall, INPUT);
  pinMode(START, INPUT_PULLUP);
  pinMode(STATUS, OUTPUT);
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);

  // Inital rand delay ensures actuator fully extends
  randPosition = 6000;

  delay(2000);
  Serial.println("Setup Complete");
}

// the loop function runs over and over again forever
void loop() {
  Serial.println("");
  Serial.println("");
  enable_circuit = digitalRead(START);
  Serial.print("BTN 1: ");
  Serial.println(enable_circuit);

  //// Reset Actuator State ////
  if (enable_circuit == 1){
    if (prevSwitchState != enable_circuit){
      Serial.println("Reseting Actuator...");
      // Extend Actuator
      Serial.println("Extending Actuator...");
      digitalWrite(STATUS, HIGH);
      digitalWrite(RELAY1, HIGH);
      digitalWrite(RELAY2, LOW);
      delay(randPosition);
      digitalWrite(STATUS, LOW);
      digitalWrite(RELAY1, LOW);
      digitalWrite(RELAY2, LOW);
      
      // Wait
      delay(1000);

      randPosition = random(6000);

      // Retract Actuator
      Serial.println("Retracting Actuator...");
      digitalWrite(STATUS, HIGH);
      digitalWrite(RELAY1, LOW);
      digitalWrite(RELAY2, HIGH);
      delay(randPosition);
      digitalWrite(STATUS, LOW);
      digitalWrite(RELAY1, LOW);
      digitalWrite(RELAY2, LOW);
      
      delay(1000);
      prevSwitchState = 1;
    }
    else{
       // Standby until button is pressed
       Serial.println("Waiting...");
    }
  }

  //// Measuring State ////
  if (enable_circuit == 0){
    if (prevSwitchState != enable_circuit){
      Serial.println("Entering Measuring Mode");
      prevSwitchState = 0;
    }
    Serial.println("Measurements");
    // Measure needle voltage
    float needleVoltage = analogRead(voutNeedle)/1024.0*5.0;
    Serial.print("Analog 0 (for needle): ");
    Serial.println(analogRead(voutNeedle)/1024.0*5.0);
  
    // Measure posterior wall voltage
    float pwVoltage = analogRead(voutPostWall)/1024.0*5.0;
    Serial.print("Analog 1 (for post wall): ");
    Serial.println(analogRead(voutPostWall)/1024.0*5.0);
    
    if (needleVoltage >= 0.5){
      Serial.println("Successful Needle Insertion");
    }else if (pwVoltage >= 0.5){
      Serial.print("Needle has punctured the vein's posterior wall");
    }else{
      Serial.println("Needle is is not in vein!");
    }
  }    
  
  delay(1000); // wait for a second
}
