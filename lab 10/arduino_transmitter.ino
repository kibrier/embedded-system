int lo_plus = 5;
int lo_minus = 6;

void setup() {
// initialize the serial communication:
Serial.begin(115200);
pinMode(lo_plus, INPUT); // Setup for leads off detection LO +
pinMode(lo_minus, INPUT); // Setup for leads off detection LO -
}
 
void loop() {
 
  if ((digitalRead(lo_plus) == 1)||(digitalRead(lo_minus) == 1)) {
    Serial.println('!');
  } else {
    // send the value of analog input 0:  
    Serial.println(analogRead(A0));
  }
  // Wait for a bit to keep serial data from saturating
  delay(100);

}
