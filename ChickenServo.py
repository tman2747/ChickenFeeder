from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
import time

class ChickenServo:
    def __init__(self, pin):
        self.factory = PiGPIOFactory()
        self.servo = Servo(pin,min_pulse_width=0.0005,max_pulse_width=0.0025,pin_factory=self.factory)
        self.angle = -270
        self.direction = True
    def moveToAngle(self, angle):
        if -270 <= angle <= 270:
            newangle = angle / 270  # Normalize angle to range [-1, 1]
            self.servo.value = newangle
            self.angle = angle
            print(newangle)
            
        else:
            print("Angle must be between 0 and 270 degrees")

    def printAngle(self):
        print(self.angle)

    def dropFood(self):
        if self.direction and self.angle >= 270:
            self.direction = False
        if not self.direction and self.angle <= -270:
            self.direction = True

        if self.direction:
            new_angle = self.angle + 80
            if new_angle > 270:
                new_angle = 270
            self.moveToAngle(new_angle)
        else:
            new_angle = self.angle - 80
            if new_angle < -270:
                new_angle = -270
            self.moveToAngle(new_angle)
        print(self.direction)
        print(self.angle)
        

def main():
    servo1=ChickenServo(17)
    servo1.servo.min()
    time.sleep(4)
    servo1.servo.max()
    time.sleep(2)

if __name__ == "__main__":
    main()