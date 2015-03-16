int xPin = A0;
int yPin = A1;
int but1Pin = 4;
int but2Pin = 7;

int xVal = 0;
int yVal = 0;
int xPrevVal = 0;
int yPrevVal = 0;

boolean but1State = 1;
boolean but2State = 1;
boolean but1PrevState = 1;
boolean but2PrevState = 1;

unsigned long time1;
unsigned long time2;

unsigned long msg;

void setup() {
  Serial.begin(9600);
  time1 = millis();
}

void loop() {
  xVal = analogRead(xPin);
  yVal = analogRead(yPin);
  
  // ADC provides a 10-bit value, but only upper 6 bits are reliable due to joystick hardware
  // Without discarding the lower bits, we will get varied readings even when physical position is unchanged
  xVal = xVal >> 4;
  yVal = yVal >> 4;
  
  // In order to provide high frequency output, we use hardware debouncing
  but1State = digitalRead(but1Pin);
  but2State = digitalRead(but2Pin);
  
  if ((xVal != xPrevVal) | 
      (yVal != yPrevVal) |
      (but1State != but1PrevState) |
      (but2State != but2PrevState)) {
    time2 = millis() - time1;
    msg = makeMsg(xVal, yVal, but1State, but2State, time2);
    
    /*
    Serial.print("time=");
    Serial.print(time2);
    Serial.print(", x=");
    Serial.print(xVal);
    Serial.print(", y=");
    Serial.print(yVal);
    Serial.print(", but1=");
    Serial.print(! but1State);
    Serial.print(", but2=");
    Serial.print(! but2State);
    Serial.print(", msg=");
    */
    Serial.println(msg, HEX);
    time1 = millis();
    
    xPrevVal = xVal;
    yPrevVal = yVal;
    but1PrevState = but1State;
    but2PrevState = but2State;    
  }
}

unsigned long makeMsg(int xVal, int yVal, boolean but1State, boolean but2State, unsigned long time2) {
  unsigned long msg = time2 << 14; // discard upper 14 bits of time
  msg += ((! but2State) << 13); // inverted logic
  msg += ((! but1State) << 12); // inverted logic
  msg += (yVal << 6);
  msg += xVal;
  return msg;
}


