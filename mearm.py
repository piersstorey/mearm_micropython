
# Imports
from time import sleep
import json
from machine import Pin
from machine import PWM

class Servo:
    """ Servo class and methods """

    def __init__(self, config):

        # Servo settings
        self.servo = config['servo']
        self.pin = config['pin']
        self.min = config['min']
        self.max = config['max']

        # Set PWM
        self.pwm = PWM(Pin(self.pin)) # Set PWM PIN
        self.pwm.freq(50) # Set PWM frequency

        """
        settings.json includes the servo name and last position
        {"base": 5660, "reach": 5230, "height": 5310, "grip": 4330}
        """
        # Open settings file
        self.json_file = open('settings.json', encoding="utf-8")
        self.settings = json.load(self.json_file)
        self.json_file.close()

        # Get previously saved servo position
        self.pos = self.settings[self.servo]

    def set_servo_cycle (self, position):
        """ Set the PWM duty """
        self.pwm.duty_u16(position)
        sleep(0.01) # Sleep for 0.01 seconds

    def move_to(self, percentage):
        """
        Move to a percentage position
        """

        pos = int((percentage * (self.max - self.min) / 100) + self.min)
        step = -30 if pos < self.pos else +30

        for duty_pos in range(self.pos, pos, step):
            self.set_servo_cycle(duty_pos)
            self.pos = duty_pos
        self.save_pos(self.servo, self.pos)

    def save_pos(self, servo, pos):
        """
        Method for saving the final duty position
        """
        self.settings[servo] = pos
        with open("settings.json", "w") as jsonFile:
            json.dump(self.settings, jsonFile)

class MeArm:
    """ MeArm class to set servo configurations"""

    def __init__(self):

        # Create each servo instance passing default values 
        self.height = Servo({'servo': 'height', 'pin': 0, 'min': 2500, 'max': 6000})
        self.reach = Servo({'servo': 'reach', 'pin': 1, 'min': 5200, 'max': 6700})
        self.grip = Servo({'servo': 'grip', 'pin': 2, 'min': 4300, 'max': 7600})
        self.base = Servo({'servo': 'base', 'pin': 3, 'min': 2600, 'max': 7000})
