
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
        self.settings = {}

        # Set PWM
        self.pwm = PWM(Pin(self.pin)) # Set PWM PIN
        self.pwm.freq(50) # Set PWM frequency

    def set_servo_cycle (self, position):
        """ Set the PWM duty """
        self.pwm.duty_u16(position)
        sleep(0.01) # Sleep for 0.01 seconds

    def move_to(self, percentage, last_pos):
        """
        Move to a percentage position
        """
        self.pos = last_pos

        pos = int((percentage * (self.max - self.min) / 100) + self.min)
        step = -30 if pos < self.pos else +30

        for duty_pos in range(self.pos, pos, step):
            self.set_servo_cycle(duty_pos)
            self.pos = duty_pos
         
    def get_pos(self):
        return self.pos


class MeArm:
    """ MeArm class to set servo configurations"""

    def __init__(self):
        
        # Set last save settings from settings.json
        self.json_file = open('settings.json', encoding="utf-8")
        self.settings = json.load(self.json_file)
        self.json_file.close()

        # Create each servo instance passing default values 
        self.height = Servo({'servo': 'height', 'pin': 0, 'min': 2500, 'max': 6000})
        self.reach = Servo({'servo': 'reach', 'pin': 1, 'min': 5200, 'max': 6700})
        self.grip = Servo({'servo': 'grip', 'pin': 2, 'min': 4300, 'max': 7600})
        self.base = Servo({'servo': 'base', 'pin': 3, 'min': 2600, 'max': 7000})
        
    def set_center(self):
        """ Set MeArm to ceter positions """
        self.set_height(10)
        self.set_reach(10)
        self.set_grip(50)
        self.set_base(50)
        
    def set_height(self, percentage):
        """ Set MeArm height """
        self.height.move_to(percentage, self.settings["height"])
        self.settings["height"] = self.height.get_pos()
        self.save_settings()
        print(self.settings)
        
    def set_reach(self, percentage):
        """ Set MeArm reach """
        self.reach.move_to(percentage, self.settings["reach"])
        self.settings["reach"] = self.reach.get_pos()
        self.save_settings()
        print(self.settings)
        
    def set_grip(self, percentage):
        """ Set MeArm grip """
        self.grip.move_to(percentage, self.settings["grip"])
        self.settings["grip"] = self.grip.get_pos()
        self.save_settings()
        print(self.settings)
        
    def set_base(self, percentage):
        """ Set MeArm base """
        self.base.move_to(percentage, self.settings["base"])
        self.settings["base"] = self.base.get_pos()
        self.save_settings()
        print(self.settings)
        
    def save_settings(self):
        """
        Save settings to settings.json file
        Settings Dict: {"base": 4820, "reach": 5230, "height": 2880, "grip": 5920}
        """
        with open("settings.json", "w") as jsonFile:
            json.dump(self.settings, jsonFile)
