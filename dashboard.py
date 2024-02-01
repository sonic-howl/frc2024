import wpilib

def lightLed( id: int, on: bool ):
    wpilib.SmartDashboard.putBoolean( f"DB/LED {id}", on )

def sendMessage( id: int, msg: str ):
    wpilib.SmartDashboard.putString( f"DB/String {id}", msg )

def button( id: int ) -> bool:
    return wpilib.SmartDashboard.getBoolean( f"DB/Button {id}", False )

def slider( id: int ) -> float:
    return wpilib.SmartDashboard.getNumber( f"DB/Slider {id}", 0.0 )