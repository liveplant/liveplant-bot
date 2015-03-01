  //Watering a plant, rotate 90 degrees while 
  
  #include <Servo.h> 
   
  Servo myservo;  // create servo object to control a servo 
  
  int pos = 0;    // variable to store the servo position 
  const int led = 13;
  const int pulse = 9;
  long lastled = 0;
  int millitime = 1000;
  int flip = 0;
   
  void setup() 
  { 
    Serial.begin(9600); // set serial speed
    myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
    myservo.write(94);
    pinMode(led, OUTPUT);
    //analogWrite(pulse, 0);
  } 
   
   
  void loop() 
  { 
    while (Serial.available() == 0); // do nothing if nothing sent
    int val = Serial.read() - '0'; // deduct ascii value of '0' to find numeric value of sent number
      
    switch (val) 
    {
      /*case 0: //block water from moving
          myservo.write(0);
          digitalWrite(led, LOW);
      break;*/
      case 1: //allow water to move
          myservo.write(180);
          delay(350);
          myservo.write(94);
          delay(10000);
          myservo.write(0);
          delay(355);
          myservo.write(94);
          digitalWrite(led, HIGH);
      break;
      case 2:
          digitalWrite(led, LOW);
      break;
    }
    Serial.println(val);
    val = 2;
  }
