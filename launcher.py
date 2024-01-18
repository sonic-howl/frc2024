import wpilib

class Launcher:

    #
    motorLeft  = wpilib.PWMTalonSRX(0)
    motorRight = wpilib.PWMTalonSRX(1)

    def launch(self, trigger):
        if trigger:
            #Launch motors must counter rotate
            self.motorLeft.set(-1.0)
            self.motorRight.set(1.0)
        else:
            #Stop motors
            self.motorLeft.set(0.0)
            self.motorRight.set(0.0)
