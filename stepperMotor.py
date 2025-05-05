import RPi.GPIO as GPIO
import time

class stepperMotor:

    def __init__(self, stepPin, directionPin):
        self.stepPin = stepPin
        self.directionPin = directionPin
        self.counter = 0 # Keeps track of how many steps we've taken (- values are CW, + values are CCW)

        GPIO.setup(self.stepPin, GPIO.OUT)
        GPIO.setup(self.directionPin, GPIO.OUT)

        GPIO.output(self.stepPin, GPIO.LOW)
        GPIO.output(self.directionPin, GPIO.LOW)

    def stepperMovement(self, steps, direction,timeDelay = 0.02):
        #__doc__
        """
        Moves a stepper motor a certain number of steps, with a delay inbetween steps

        steps (int): the amount of steps to take for the stepper

        direction (string): "CW" makes the motor run clock wise, "CCW" makes the motor run counter clock wise

        timeDelay (float): defines a delay time (initially 0.02 sec)
        """

        if(direction == "CW"):
            GPIO.output(self.directionPin, GPIO.HIGH)
        else:
            GPIO.output(self.directionPin, GPIO.LOW)

        for i in range(steps):
            GPIO.output(self.stepPin, GPIO.LOW)
            time.sleep(time)
            GPIO.output(self.stepPin, GPIO.HIGH)

            if(direction == "CW"):
                self.counter -= 1
            else:
                self.counter += 1

            time.sleep(timeDelay)
