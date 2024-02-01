import wpilib

# Treat controller instances as private, use the functions below to access controls.
pilot = wpilib.PS4Controller(0);
#engineer = TBD

def driveCommand() -> float:
    return pilot.getLeftY()

def strafeCommand() -> float:
    return pilot.getLeftX()
    
def rotationCommand() -> float:
    return pilot.getRightX()
    
def pickupCommand() -> bool:
    return pilot.getL1Button()

def shootCommand() -> bool:
    return pilot.getR1Button()
    