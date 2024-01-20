import wpilib

def lightLed( id: int, on: bool ):
    wpilib.SmartDashboard.putBoolean( f"DB/LED {id}", on )