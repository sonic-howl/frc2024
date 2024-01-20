import wpilib
import driveteam
import dashboard
import subsystems

class MyRobot(wpilib.TimedRobot):

    testmotors = subsystems.ControllerTest()

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
        # Collect inputs
        cmdX = driveteam.strafeCommand()
        cmdY = driveteam.speedCommand()
        cmdZ = driveteam.rotationCommand()

        intake  = driveteam.pickupCommand()
        trigger = driveteam.shootCommand()

        # Issue Commands
        self.testmotors.move( cmdX, cmdY, cmdZ )
        self.testmotors.pickup( intake )
        self.testmotors.shoot( trigger )

        # Update dahboard
        dashboard.lightLed( 0, intake )
        dashboard.lightLed( 1, trigger )

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