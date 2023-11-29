from time import sleep

from mearm import MeArm
me_arm = MeArm()
me_arm.set_center()
sleep(1)
me_arm.set_height(20)
me_arm.set_reach(100)
me_arm.set_grip(96)
me_arm.set_height(90)
me_arm.set_base(70)
me_arm.set_grip(10)
me_arm.set_reach(10)

