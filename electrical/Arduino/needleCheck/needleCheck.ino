const int voutPin0 = A0;
const int voutPin1 = A1;
const int voutPin2 = A2;
const int voutPin3 = A3;
const int voutPin4 = A4;

void setup() {
  Serial.begin(9600);
  delay(2);
  pinMode(voutPin0, INPUT);
  pinMode(voutPin1, INPUT);
  pinMode(voutPin2, INPUT);
  pinMode(voutPin3, INPUT);
  pinMode(voutPin4, INPUT);

  delay(2000);
  Serial.println("Setup Complete");
}

// the loop function runs over and over again forever
void loop() {
  Serial.print("Analog 0: ");
  Serial.println(analogRead(voutPin0));
  Serial.print("Analog 1: ");
  Serial.println(analogRead(voutPin1));
  Serial.print("Analog 2: ");
  Serial.println(analogRead(voutPin2));
  Serial.print("Analog 3: ");
  Serial.println(analogRead(voutPin3));
  Serial.print("Analog 4: ");
  Serial.println(analogRead(voutPin4));
  delay(1000);                          // wait for a second
}
