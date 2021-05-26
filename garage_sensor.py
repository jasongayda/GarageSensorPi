import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)


# DISTANCE VARIABLES IN INCHES
minDistance = 5
maxDistance = 15

# DISTANCE THAT WE START DETECTING OBJECTS
startMeasure = 25

# SET GPIO PINS
# PINS FOR DISTANCE SENSOR
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
# PINS FOR LEDS
GPIO_RED = 17
GPIO_GREEN = 22
GPIO_BLUE = 27

# SET GPIO DIRECTION (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# PINS FOR LEDS
GPIO.setup(GPIO_RED, GPIO.OUT)
GPIO.setup(GPIO_GREEN, GPIO.OUT)
GPIO.setup(GPIO_BLUE, GPIO.OUT)

 
def distance():
    # SET TRIGGER TO HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # SET TRIGGER AFTER 0.01MS TO LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # SAVE STARTTIME
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # SAVE STOPTIME
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # TIME DIFFERENCE BETWEEN START AND STOP
    TimeElapsed = StopTime - StartTime
    
    # MULTIPLY WITH THE SONIC SPEED (34300 cm/s)
    # AND DIVIDE BY 2, (FROM SENSOR AND BACK TO SENSOR)
    # CONVERT TO INCHES (/ 2.54)
    distance = (TimeElapsed * 34300 / 2.54) / 2
 
    return distance
 

if __name__ == '__main__':
    try:
        while True:
            dist = distance()

            print ("Measured Distance = %.1f inches" % dist)

            if dist < minDistance:
                print ("Too Close!")

                # BLINK RED LED RAPIDLY
                GPIO.output(GPIO_RED, True)
                time.sleep(0.1)
                GPIO.output(GPIO_RED, False)

                # TURN OFF GREEN LED
                GPIO.output(GPIO_GREEN, False)

                # TURN ON THE BLUE LED
                GPIO.output(GPIO_BLUE, False)

            elif dist > minDistance and dist < maxDistance:
                print ("In Range")

                # TURN OFF RED LED
                GPIO.output(GPIO_RED, False)

                # TURN ON GREEN LED
                GPIO.output(GPIO_GREEN, True)

                # TURN OFF BLUE LED
                GPIO.output(GPIO_BLUE, False)
   
            elif dist < startMeasure:
                print ("Object Detected")

                # TURN OFF RED LED
                GPIO.output(GPIO_RED, False)

                # TURN ON GREEN LED
                GPIO.output(GPIO_GREEN, False)

                # TURN ON BLUE LED
                GPIO.output(GPIO_BLUE, True)
            elif dist > startMeasure:
                print ("No Objects Detected")

                # ALL LEDS OFF
                GPIO.output(GPIO_RED, False)
                GPIO.output(GPIO_GREEN, False)
                GPIO.output(GPIO_BLUE, False)
            time.sleep(.25)
 
        # KILL BY PRESSING CNTRL-C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()