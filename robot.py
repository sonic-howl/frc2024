import wpilib
import driveteam
import launcher
import mechanisms

class MyRobot(wpilib.TimedRobot):

    DT = driveteam.DriveTeam()

    shooter    = launcher.Launcher()
    testmotors = mechanisms.ControllerTest()

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
        # Bogus motion
        cmdX = self.DT.getStrafeCommand()
        cmdY = self.DT.getSpeedCommand()
        cmdZ = self.DT.getRotationCommand()
        self.testmotors.move( cmdX, cmdY, cmdZ )

        # Shoot notes
        trigger = self.DT.getShootCommand()
        self.shooter.launch(trigger)

    def teleopExit(self):
        # Stop the shooter
        self.shooter.launch(False)
        self.swervedrive.stop()

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