#define STATUS 11
#define RELAY1 12
#define RELAY2 13

long randPosition = 0;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
    pinMode(STATUS, OUTPUT);
    pinMode(RELAY1, OUTPUT);
    pinMode(RELAY2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  randPosition = random(6000);
//  randPosition = 6000;

  // Retract Actuator
  digitalWrite(STATUS, HIGH);
  digitalWrite(RELAY1, HIGH);
  digitalWrite(RELAY2, LOW);
  delay(randPosition);
  digitalWrite(STATUS, LOW);
  digitalWrite(RELAY1, LOW);
  digitalWrite(RELAY2, LOW);

  // Wait
  delay(5000);

  // Extend Actuator
  digitalWrite(STATUS, HIGH);
  digitalWrite(RELAY1, LOW);
  digitalWrite(RELAY2, HIGH);
  delay(randPosition);
  digitalWrite(STATUS, LOW);
  digitalWrite(RELAY1, LOW);
  digitalWrite(RELAY2, LOW);

  // Wait
  delay(5000);
}
