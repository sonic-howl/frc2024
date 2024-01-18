import wpilib

class Operators:

    pilot = wpilib.PS4Controller(0); #pilot controller on port 0
    #engineer = TBD

    # Return positive values to move forward, negatives values reverse
    def getSpeedCommand(self) -> float:
        return self.pilot.getLeftY()

    def getStrafeCommand(self) -> float:
        return self.pilot.getLeftX()
    
    def getRotationCommand(self) -> float:
        return self.pilot.getRightX()
    
    def getShootCommand(self) -> bool:
        return self.pilot.getR1Button()
    