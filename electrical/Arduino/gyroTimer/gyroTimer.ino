/**
* @file QBitCode.ino
* @author QBit Electrical Team (IV Tutor)
* @brief Measure voltage to determine if the needle has entered the vein.
* @version 1.0
* @date 2024-03-10
* 
*/

#include <Wire.h>

//Pin variables
const int voutPin0 = A0;
const int voutPin1 = A1;
const int voutPin2 = 5;

//Accelerometer
const int MPU_addr = 0x68;

//Timer variables
int timer = 0;
bool timerStart = false;
bool started = false;
 
void setup() {
  //Inital setup of pins and serial monitor
  Serial.begin(9600);
  delay(2);
  pinMode(voutPin0, INPUT);
  pinMode(voutPin1, INPUT);
  pinMode(voutPin2, INPUT);
 
  //Start switch on high
  digitalWrite(voutPin2, HIGH);
 
  //Initialize I2C communication
  Wire.begin();
 
  //Wake up the MPU-6050
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);
  Wire.write(0);    
  Wire.endTransmission(true);
  delay(2000);
  Serial.println("Setup Complete");
}
 
 
 
//Accelerometer & Gyro
void accGyro () {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // Start with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  //Wire.requestFrom((uint8_t)MPU_addr, (size_t)14, true);  // Request 14 registers (Accel + Temp + Gyro)
 
 
  //Read accelerometer data
  int16_t AccX = Wire.read() << 8 | Wire.read();
  int16_t AccY = Wire.read() << 8 | Wire.read();
  int16_t AccZ = Wire.read() << 8 | Wire.read();
 
 
  // Convert accelerometer data to m/s²
  float AccX_mps2 = (float)AccX / 16384.0 * 9.81;
  float AccY_mps2 = (float)AccY / 16384.0 * 9.81;
  float AccZ_mps2 = (float)AccZ / 16384.0 * 9.81;
 
 
  //Skip the temperature data (not used in this example)
  Wire.read(); Wire.read();
 
 
  //Read gyroscope data
  int16_t GyroX = Wire.read() << 8 | Wire.read();
  int16_t GyroY = Wire.read() << 8 | Wire.read();
  int16_t GyroZ = Wire.read() << 8 | Wire.read();
 
 
  //Convert gyroscope data to degrees/sec
  float GyroX_dps = (float)GyroX / 131.0;
  float GyroY_dps = (float)GyroY / 131.0;
  float GyroZ_dps = (float)GyroZ / 131.0;
 
  //Display the converted values
  //Serial.print("AccX (m/s²) = "); Serial.print(AccX_mps2);
  //Serial.print(" | AccY (m/s²) = "); Serial.print(AccY_mps2);
  //Serial.print(" | AccZ (m/s²) = "); Serial.println(AccZ_mps2);
  Serial.print("GyroX (°/s) = "); Serial.print(GyroX_dps);
  Serial.print(" | GyroY (°/s) = "); Serial.print(GyroY_dps);
  Serial.print(" | GyroZ (°/s) = "); Serial.println(GyroZ_dps);
}
 
 
 
 

//The loop function runs over and over again forever
void loop() {
  //Check if switch is pushed
  if(digitalRead(voutPin2) == LOW) {
    timerStart = true;
  } else
    timerStart = false;
  }
 
  //Start incrementing time
  if(timerStart) {
    timer++;
    Serial.print("Timer = ");
    Serial.print(timer);
    Serial.println(" seconds");
    started = true;
  }
 
  //Print final time
  if(timerStart == false && started == true) {
    Serial.print("Final time: ");
    Serial.print(timer);
    Serial.println(" seconds");
  }
  //Call gyro
  accGyro();
 
  
  //Measure needle voltage
  float needleVoltage = analogRead(voutPin0)/1024*5.0;
  Serial.print("Analog 0: ");
  Serial.println(analogRead(voutPin0)/1024*5.0);
  //Measure posterior wall voltage
  float pwVoltage = analogRead(voutPin1)/1024*5.0;
  Serial.print("Analog 1: ");
  Serial.println(analogRead(voutPin1)/1024*5.0);
  if (needleVoltage >= 0.5){
    Serial.println("Successful Needle Insertion");
  }else if (pwVoltage >= 0.5){
    Serial.print("Needle has punctured the vein's posterior wall");
  }else{
    Serial.println("Needle is is not in vein!");
  }
 
  //Wait for a second
  delay(1000);
}
