import wpilib

import drivestation
import driveteam
import launcher


class MyRobot(wpilib.TimedRobot):
  copilots = driveteam.DriveTeam()
  pilots = driveteam.DriveTeam()
  strafe = 0.0
  turn = 0.0
  drive = 0.0

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
    self.strafe = self.pilots.get_strafe_commands()
    self.turn = self.pilots.get_turn_commands()
    self.drive = self.pilots.get_drive_commands()
    self.winch = self.pilots.get_winch_commands()
    self.hookextend = self.pilots.get_hook_extension_commands()
    self.hookretract = self.pilots.get_hook_retract_commands()
    self.hookleft = self.pilots.get_hook_left_commands()
    self.hookright = self.pilots.get_hook_right_commands()

    self.aim = self.copilots.get_aim_commands()
    self.fire = self.copilots.get_firing_commands()
    self.unjam = self.copilots.get_unjam_commands()
    self.pickup = self.copilots.get_pickup_commands()
    self.eject = self.copilots.get_eject_commands()
    drivestation.light_0(self.winch)
    drivestation.light_1(self.drive)
    drivestation.light_2(self.fire)
    drivestation.light_3(self.pickup)

    # Launcher
    launcher.shoot(self.fire)
    launcher.elevate(self.aim)

  def teleopExit(self):
    launcher.stop()

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
