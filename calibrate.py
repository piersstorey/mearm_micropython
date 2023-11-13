
# Imports
from time import sleep
import json
from machine import Pin
from machine import PWM

"""
Module and class for servo calibration
DO NOT CONNECT SERVO's TO THE MeArm

Servo positions when fitted
Servo         Min   Max
servo_height  2000  6000
servo_reach   5200  6700
servo_grip    4300  7600
servo_base    2000  7000

Servo positions
max = 8200
mid = 4800
min = 1200
"""

class Servo:

    def __init__(self, config):

        # Config n ting
        self.servo = config['servo']
        self.pin = config['pin']
        self.min = config['min']
        self.mid = config['mid']
        self.max = config['max']

        # Set PWM
        self.pwm = PWM(Pin(self.pin)) # Set PWM PIN
        self.pwm.freq(50) # Set PWM frequency

        # Open settings file
        self.json_file = open('settings.json', encoding="utf-8")
        self.settings = json.load(self.json_file)

        self.pos = None

    def set_servo_cycle (self, position):
        self.pwm.duty_u16(position)
        sleep(0.01)

    def set_to_center(self):

        """
        This method is used for calibration. Make sure your
        servo's are not connected to your MeArm
        You may need to adjust the values based on your servo
        """

        for pos in range(self.max,self.mid,-50):
            self.set_servo_cycle(pos)

        for pos in range(self.min,self.mid,50):
            self.set_servo_cycle(pos)

        self.pos = self.mid
        self.save_pos(self.servo, self.pos)

    def move_to_min(self):
        for pos in range(self.pos,self.min,-50):
            self.pos = pos
            self.set_servo_cycle(pos)

    def move_to_max(self):
        for pos in range(self.pos,self.max,50):
            self.pos = pos
            self.set_servo_cycle(pos)

    def move_to_mid(self):
        step = -50 if self.pos > self.mid else +50          
        for pos in range(self.pos,self.mid,step):
            self.pos = pos
            self.set_servo_cycle(pos)

    def save_pos(self, servo, pos):
        self.settings[servo] = pos
        with open("settings.json", "w") as jsonFile:
            json.dump(self.settings, jsonFile)

# Servo min, max, mid set to un-fitted servo
servo = Servo({'servo': 'height', 'pin': 0, 'min': 1200, 'max': 8200, 'mid': 4800})
servo.set_to_center()
