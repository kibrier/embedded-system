int analogPin = 14;
int data = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  data = analogRead(analogPin);
  Serial.println(data);
  delay(10);
}
