#include "Car.h"

Car car;

//This will run once at startup
void setup()
{
  /* Inits the car using:
   *  Pin 10 for steering
   *  Pin 11 for throttle
   *  90 for the neutral value
   */
  car.InitCar(10, 11, 90);

  //Sets steering and throttle to neutral
  car.goNeutral();
  
  //Enable serial data transfer
  Serial.begin(9600);

  #ifdef DEBUG
  Serial.write(("Steering range: " 
                + String(car.MIN_STEER) + "-" + car.MAX_STEER
                + "\tThrottle range: "
                + car.MIN_THROTTLE + "-" + car.MAX_THROTTLE
                + "\nEnter your commands. The format is: <Steering Value><White Space><Throttle Value>\n\n").c_str());
  #endif
}

//This will loop endlessly as long as the arduino is powered
void loop()
{
  //Variables to store serial input
  int steerValue;
  int throttleValue;

  //Check if there is any data waiting in the Serial buffer
  if (Serial.available() > 0)
  {
    //Read the incoming data and parse it as an int
    steerValue = Serial.parseInt();
    throttleValue = Serial.parseInt();

    //If either is a negative number, set car to neutral
    if (steerValue < 0 || throttleValue < 0)
    {
      car.goNeutral();
      
      #ifdef DEBUG
      Serial.write("Car set to neutral\n");
      #endif
    }
    else //Use those values as the new values for the steering and throttle
    {
      car.setSteering(steerValue);
      car.setThrottle(throttleValue);

      #ifdef DEBUG
      Serial.write(("Steering: " + String(steerValue)
                    + "\tThrottle: " +  String(throttleValue) + "\n").c_str());
      #endif
    }
  }
}

