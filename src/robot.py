import wpilib

import drivestation
import driveteam
import swerve.swervesubsystem
import utils.utils

class MyRobot(wpilib.TimedRobot):
  pilots = driveteam.DriveTeam()
  drivebase = swerve.swervesubsystem.SwerveSubsystem()
  def __init__(self):
    self.strafe = 0.0
    self.turn = 0.0
    self.drive = 0.0
    self.winch = False
    self.hookextend = False
    self.hookretract = False
    self.hookleft = False
    self.hookright = False

    self.aim = 0.0
    self.fire = 0.0
    self.unjam = False
    self.pickup = 0.0
    self.eject = False
    wpilib._wpilib.TimedRobot.__init__(self)

  def getInputs(self):
    self.strafe = self.pilots.get_strafe_command()
    self.turn = self.pilots.get_turn_command()
    self.drive = self.pilots.get_drive_command()
    self.winch = self.pilots.get_winch_command()
    self.hookextend = self.pilots.get_hook_extension_command()
    self.hookretract = self.pilots.get_hook_retract_command()
    self.hookleft = self.pilots.get_hook_left_command()
    self.hookright = self.pilots.get_hook_right_command()

    self.aim = self.pilots.get_aim_command()
    self.fire = self.pilots.get_firing_command()
    self.unjam = self.pilots.get_unjam_command()
    self.pickup = self.pilots.get_pickup_command()
    self.eject = self.pilots.get_eject_command()

  def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """

  def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""

  def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""

  def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""

  def teleopPeriodic(self):
    """This function is called periodically during teleoperated mode."""
    self.getInputs()
    drivestation.setDBLED("0", self.unjam)
    drivestation.setDBLED("1", self.eject)

    wpilib.SmartDashboard.putString("DB/String 0", str(self.drivebase.getRotation2d()))
    # drivestation.light_2(self.fire)
    # drivestation.light_3(self.pickup)

    # drive base
    magnitude = abs(self.strafe) + abs(self.drive) + abs(self.turn)
    if utils.utils.dz(magnitude) > 0:
      self.drivebase.setvelocity(self.drive, self.strafe, self.turn)
    else:
      self.drivebase.stop()


  def testInit(self):
    """This function is called once each time the robot enters test mode."""

  def testPeriodic(self):
    """This function is called periodically during test mode."""

  # def simulationInit(self):
  #   """This function is called once each time the robot enters simulation mode."""

  # def simulationPeriodic(self):
  #   """This function is called periodically during simulation mode."""


if __name__ == "__main__":
  wpilib.run(MyRobot)
