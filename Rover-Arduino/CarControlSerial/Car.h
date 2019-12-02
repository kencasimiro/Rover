#include <Servo.h>

#include "Define.h"

class Car
{
  public:
    //Constructor
    Car(): ABS_MAX_THROTTLE(140), ABS_MIN_THROTTLE(40),
           ABS_MAX_STEER(140), ABS_MIN_STEER(53),
           MAX_THROTTLE(105), MIN_THROTTLE(75),
           MAX_STEER(ABS_MAX_STEER), MIN_STEER(ABS_MIN_STEER)
    {
      neutralValue = 0;
    }

    //Arduino has issues with placing code in the constructor so we use this 
    //  to initialize instead
    void InitCar(const int& steeringPin, const int& throttlePin, const int& neutralValue)
    {
      //Attaches the pins to the servo objects
      steer.attach(steeringPin);
      throttle.attach(throttlePin);

      this->neutralValue = neutralValue;
    }

    //Sets throttle and steering to neutral
    void goNeutral()
    {
      this->setSteering(neutralValue);
      this->setThrottle(neutralValue);
    }

    //Sets the throttle over time instead of right away
    void setThrottle(int value)
    {
      //Check that value is within a valid range
      //  If not, correct it
      if (value < MIN_THROTTLE)
      {
        #ifdef DEBUG
        outputError(value, MIN_THROTTLE);
        #endif
        value = MIN_THROTTLE;
      }
      else if (value > MAX_THROTTLE)
      {
        #ifdef DEBUG
        outputError(value, MAX_THROTTLE);
        #endif
        value = MAX_THROTTLE;
      }

      //Reads the current value from the throttle
      int currentVal = throttle.read();

      //Checks whether the value needs to be increased or decreased
      //  Then uses a for loop to change the value over time
      if (value > currentVal)
        for (currentVal; currentVal <= value; currentVal++)
        {
          wait(WAIT_TIME);
          throttle.write(currentVal);
        }
      else
        for (currentVal; currentVal >= value; currentVal--)
        {
          wait(WAIT_TIME);
          throttle.write(currentVal);
        }
    }

    //Sets steering value
    void setSteering(int value)
    {
      //Checks that value is within a valid range
      //  If not, correct it
      if (value > MAX_STEER)
      {
        #ifdef DEBUG
        outputError(value, MAX_STEER);
        #endif
        value = MAX_STEER;
      }
      else if (value < MIN_STEER)
      {
        #ifdef DEBUG
        outputError(value, MIN_STEER);
        #endif
        value = MIN_STEER;
      }

      steer.write(value);
    }

    #ifdef DEBUG
    //Used to tell user input is out of range
    void outputError(const int& badValue, const int& newValue) const
    {
      Serial.write((String(badValue) + " is not within range. Setting to " + newValue + ".\n").c_str());
    }
    #endif

    //Loops until passed in amount of milliseconds have passed
    void wait(const unsigned long& timeToWait)
    {
      unsigned long time = millis();

      //While time passed is less than timeToWait, continue to loop
      while( millis() - time < timeToWait ) {}
    }

    //Absoulte limits imposed by the hardware on the throttle and steering
    const int ABS_MAX_THROTTLE;  //Forward
    const int ABS_MIN_THROTTLE;  //Reverse
    const int ABS_MAX_STEER;     //Left
    const int ABS_MIN_STEER;     //Right

    //Limits imposed by the user on the throttle and steering
    const int MAX_THROTTLE;
    const int MIN_THROTTLE;
    const int MAX_STEER;
    const int MIN_STEER;

  private:
    int neutralValue;
    Servo steer;
    Servo throttle;

    //Amount of milliseconds to wait for
    const unsigned long WAIT_TIME = 15UL;
};
