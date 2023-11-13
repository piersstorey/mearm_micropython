""" Main module to control your MeArm """

from mearm import MeArm

me_arm = MeArm()
# Example method calls using 0 - 100% servo movement
me_arm.height.move_to(100)
me_arm.reach.move_to(60)
me_arm.grip.move_to(0)
me_arm.base.move_to(70)
