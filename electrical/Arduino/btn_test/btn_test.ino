#define START 4

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(START, INPUT_PULLUP);

  Serial.println("Setup Complete");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("BTN 1: ");
  Serial.println(digitalRead(START));
}
