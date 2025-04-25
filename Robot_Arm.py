from stepperMotorTest import stepperMotor
import threading
import msvcrt
import time


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

baseStepperPins = [0,0]
jointOnePins = [0,0]
jointTwoPins = [0,0]

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

def get_immediate_input():
    if msvcrt.kbhit():
        return msvcrt.getch().decode("utf-8")
    return None

def main():
    robot = Robot_Arm()
    counter = 0
    while True:
        key = get_immediate_input()

        if key == "d":
            robot.moveBaseStepper(4, "CW",None)

        if key == "a":
            robot.moveBaseStepper(4, "CCW",None)

        if key == "w":
            robot.moveJointOne(4,"CW",None)
        
        if key == "s":
            robot.moveJointOne(4,"CCW", None)

        if key =="i":
            robot.moveJointTwo(4, "CW", None)

        if key == "k":
            robot.moveJointTwo(4, "CCW", None)

        if key == "c":
            robot.setCounterToZero()

        counter +=1
        if (counter % 100 == 0):
            print(robot)
        
        time.sleep(0.01)
            

if __name__ == "__main__":
    main()