from stepperMotor import stepperMotor
import threading
import sys
import tty
import termios
import time
import os
import RPi.GPIO as GPIO

'''
Robot Arm Project:

       /        |
      /         |
      |         /                    y
       | ______/                     ^
          { }    Second Joint        |
          / /                        |
         / /                         |
        / /                          |
       { }      First Joint          |
       | |                           |
       | |                           |
       | |                           |   Z
 ______|_|____                       |  /
/             |                      | /
|     Base    |                      |/
|_____________|                      |-------------------------->  x

Base rotates around the y axis
First joint rotates around the x axis
Second joint rotates around the x axis

'''

baseStepperPins = [3,5]
jointOnePins = [7,8]
jointTwoPins = [11,13]

buttons = [13,15,16,18]

class Robot_Arm():

    def __init__(self):
        self.baseStepper = stepperMotor(baseStepperPins)

        self.jointOne = stepperMotor(jointOnePins)

        self.jointTwo = stepperMotor(jointTwoPins)

        self.motors = [self.baseStepper, self.jointOne, self.jointTwo]

    def __str__(self):
        return f'Motors:\n---------------------------\nBase: \n  {self.baseStepper}\nJoint One:\n  {self.jointOne}\nJoint Two:\n {self.jointTwo}\n'

    def setCounterToZero(self):
        for motor in self.motors:
            motor.counter = 0

    def moveBaseStepper(self, steps, direction, timeDelay = None):
        self.baseStepper.stepperMovement(steps, direction, timeDelay, )

    def moveJointOne(self, steps, direction, timeDelay = None):
        self.jointOne.stepperMovement(steps, direction, timeDelay, )

    def moveJointTwo(self, steps, direction, timeDelay = None):
        self.jointTwo.stepperMovement(steps, direction, timeDelay, )

    def moveMotor(self, motor, steps, direction, timeDelay = None):
        self.motors[motor].stepperMovement(steps, direction, timeDelay, )

    def moveToLocation(self, angles):
        for i, angle in enumerate(angles):
            self.motors[i].stepperMoveToAngle(angle)
    
    def robotReset(self):
        for motor in self.motors:
            motor.moveToAngleZero()

    def printDiagnositcs(self):

        angles = [motor.calculateAngleDegrees() for motor in self.motors]
        steps = [motor.counter for motor in self.motors]

        print("" \
        "Diagnostics:\n" "")
        print("{:<20}{:<20}{:<20}{:<20}".format("Data","|Base Motor|", "|Joint 1 Motor|", "|Joint 2 Motor|"))
        print("-"*80)
        print("{:<20}".format("Steps") + f'{steps[0]:<20}{steps[1]:<20}{steps[2]:<20}\n')
        print("{:<20}".format("Angles") + f'{angles[0]:<20}{angles[1]:<20}{angles[2]:<20}\n')


def get_immediate_input():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def manualControl(robot):
    key = get_immediate_input()

    if key == "d":
        robot.moveBaseStepper(2, "CW",None)

    if key == "a":
        robot.moveBaseStepper(2, "CCW",None)

    if key == "w":
        robot.moveJointOne(2,"CW",None)
    
    if key == "s":
        robot.moveJointOne(2,"CCW", None)

    if key =="i":
        robot.moveJointTwo(2, "CW", None)

    if key == "k":
        robot.moveJointTwo(2, "CCW", None)

    if key == "t":
        print(robot)

    if key == "c":
        robot.setCounterToZero()

    return key

def buttonControl(robot):
    if (GPIO.input(buttons[0]) == GPIO.LOW):
        robot.moveBaseStepper(2, "CW", None)

    if (GPIO.input(buttons[1]) == GPIO.LOW):
        robot.moveBaseStepper(2, "CCW", None)
    
    if (GPIO.input(buttons[2]) == GPIO.LOW):
        robot.moveJointOne(2,"CW", None)

    if (GPIO.input(buttons[3]) == GPIO.LOW):
        robot.moveJointOne(2,"CCW", None)
    time.sleep(0.05)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_terminal()

def main():
    GPIO.setmode(GPIO.BOARD)
    robot = Robot_Arm()
    while True:

        print("" \
        "Robot Operation\n" \
        "-------------------\n" \
        "Options:\n" \
        "1 : Manual Robot Control\n" \
        "2 : Reset Robot's Sensor Position\n" \
        "3 : Reset Robot to Base Position\n" \
        "4 : Print Diagnostics\n"
        "5 : Button Control\n"
        "q : Exit Program\n"
        )

        choice = input()

        clear_terminal()

        if(choice == "1"):
            print("To exit, press q")
            while True:
                key = manualControl(robot)

                if(key == "q"):
                    break

        elif(choice == "2"):
            robot.setCounterToZero()
            print("\nRobot Position Reset\n")

        elif(choice == '3'):
            robot.robotReset()

        elif(choice == '4'):
            robot.printDiagnositcs()

        elif(choice == '5'):
            while True:
                buttonControl(robot)

        elif(choice == "q"):
            print("Exiting")
            break
        else:
            print("Invalid key, please retry")
        
        time.sleep(0.01)
            

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Quiting by keyboard interrupt")