import wpilib
import driveteam

class MyRobot(wpilib.TimedRobot):

    DT = driveteam.Operators()
  
    #def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """

    #def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""

    #def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""

    #def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""

    def teleopPeriodic(self):
        cmdX = self.DT.getStrafeCommand()
        cmdY = self.DT.getSpeedCommand()
        cmdZ = self.DT.getRotationCommand()
        shoot = self.DT.getShootCommand()
        #print( f"Y: {cmdY}, X: {cmdX}, Z: {cmdZ}")
        if shoot:
          print( "SHOOT" )

    def teleopExit(self):
        pass

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def testExit(self):
        pass

  # def simulationInit(self):
  #   """This function is called once each time the robot enters simulation mode."""

  # def simulationPeriodic(self):
  #   """This function is called periodically during simulation mode."""


if __name__ == "__main__":
  wpilib.run(MyRobot)