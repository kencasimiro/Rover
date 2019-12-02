#include <Wire.h>

#include "Car.h"

const int POT_PIN = 0;
const int NEUTRAL_VALUE = 90;
Car car;

void setup() {
  Wire.begin(0x2a);             
  Wire.onReceive(receiveEvent);
  //Serial.begin(9600);

    /* Inits the car using:
   *  Pin 10 for steering
   *  Pin 11 for throttle
   *  90 for the neutral value
   */
  car.InitCar(10, 11, NEUTRAL_VALUE);

  //Sets steering and throttle to neutral
  car.goNeutral();
}

void loop() {}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  int value = analogRead(POT_PIN);

  int maxT = NEUTRAL_VALUE + (value/1023.0 * 50);
  int minT = NEUTRAL_VALUE - (value/1023.0 * 50);
  //Serial.println(String(maxT) + "\t" + minT);

  if(car.getMaxThrottle() != maxT)
    car.setMaxThrottle(maxT);
    
  if(car.getMinThrottle() != minT)
    car.setMinThrottle(minT);
  
  while (Wire.available()) 
  {
    int steering = Wire.read();
    int throttle = Wire.read();

    if(car.getSteering() != steering)
      car.setSteering(steering);
    
    if(car.getThrottle() != throttle)
      car.setThrottle(throttle);
    //Serial.println("Steering: " + String(steering) + "\tThrottle: " + throttle);      // print the character
  }
}
