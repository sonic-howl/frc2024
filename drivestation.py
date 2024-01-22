import wpilib


def setDBLED(LED, on):
    wpilib.SmartDashboard.putBoolean("DB/LED " + LED ,on)

def getDBLED(LED):
    return wpilib.SmartDashboard.getBoolean("DB/LED " + LED, None)