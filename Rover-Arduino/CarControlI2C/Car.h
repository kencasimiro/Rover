#include <Servo.h>

class Car
{
  public:
    //Constructor
    Car(): ABS_MAX_THROTTLE(140), ABS_MIN_THROTTLE(40),
           ABS_MAX_STEER(140), ABS_MIN_STEER(53),
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

      minThrottle = 80;
      maxThrottle = 100;      
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
      if (value < minThrottle)
      {
        value = minThrottle;
      }
      else if (value > maxThrottle)
      {
        value = maxThrottle;
      }

      throttle.write(value);
    }

    //Sets steering value
    void setSteering(int value)
    {
      //Checks that value is within a valid range
      //  If not, correct it
      if (value > MAX_STEER)
      {
        value = MAX_STEER;
      }
      else if (value < MIN_STEER)
      {
        value = MIN_STEER;
      }

      steer.write(value);
    }

    int getSteering()
    {
      return steer.read();
    }

    int getThrottle()
    {
      return throttle.read();
    }

    void setMinThrottle(const int& value)
    {
      minThrottle = value;
    }

    void setMaxThrottle(const int& value)
    {
      maxThrottle = value;
    }

    int getMinThrottle() const
    {
      return minThrottle;
    }

    int getMaxThrottle() const
    {
      return maxThrottle;
    }

    //Absoulte limits imposed by the hardware on the throttle and steering
    const int ABS_MAX_THROTTLE;  //Forward
    const int ABS_MIN_THROTTLE;  //Reverse
    const int ABS_MAX_STEER;     //Left
    const int ABS_MIN_STEER;     //Right

    //Limits imposed by the user on steering
    const int MAX_STEER;
    const int MIN_STEER;

  private:
    int neutralValue;
    int maxThrottle;
    int minThrottle;
    Servo steer;
    Servo throttle;
};
