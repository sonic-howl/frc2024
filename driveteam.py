import wpilib

class Operators:

    pilot = wpilib.PS4Controller(0); #pilot controller on port 0
    #engineer = TBD

    # Return positive values to move forward, negatives values reverse
    def getSpeedCommand(self) -> float:
        y = self.pilot.getLeftY();
        return y

    def getStrafeCommand(self) -> float:
        x = self.pilot.getLeftX();
        return x
    
    def getRotationCommand(self) -> float:
        z = self.pilot.getRightX()
        return z
    