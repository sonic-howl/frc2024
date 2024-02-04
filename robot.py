import wpilib
from cscore import CameraServer
from cscore import VideoMode

import dashboard
import driveteam
import swerve.swervesubsystem
import utils.utils

class MyRobot(wpilib.TimedRobot):

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
    self.strafe = driveteam.strafe_command()
    self.turn = driveteam.turn_command()
    self.drive = driveteam.drive_command()
    #self.winch = driveteam.get_winch_command()
    #self.hookextend = driveteam.get_hook_extension_command()
    #self.hookretract = driveteam.get_hook_retract_command()
    #self.hookleft = driveteam.get_hook_left_command()
    #self.hookright = driveteam.get_hook_right_command()

    #self.aim = driveteam.get_aim_command()
    self.fire = driveteam.launch_command()
    self.unjam = driveteam.unjam_command()
    self.pickup = driveteam.pickup_command()
    self.eject = driveteam.eject_command()

  def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """
    # CameraServer.launch will immediately return in simulation
    #wpilib.cameraserver.CameraServer.launch()
    usbCam = CameraServer.startAutomaticCapture()
    usbCam.setVideoMode( VideoMode.PixelFormat.kMJPEG, 640, 480, 30 )
    

  def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""

  def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""

  def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""

  def teleopPeriodic(self):
    """This function is called periodically during teleoperated mode."""
    self.getInputs()

    # drive base
    magnitude = abs(self.strafe) + abs(self.drive) + abs(self.turn)
    if utils.utils.dz(magnitude) > 0:
      self.drivebase.setvelocity( self.drive, self.strafe, self.turn )
    else:
      self.drivebase.stop()

    # Update dahboard
    dashboard.light_led( 0, self.pickup )
    dashboard.light_led( 1, self.fire )
    dashboard.light_led( 2, self.eject )
    dashboard.light_led( 3, self.unjam )

  def testInit(self):
    """This function is called once each time the robot enters test mode."""

  def testPeriodic(self):
    """This function is called periodically during test mode."""

  #def simulationInit(self):
  #  """This function is called once each time the robot enters simulation mode."""

  #def simulationPeriodic(self):
  #  """This function is called periodically during simulation mode."""


if __name__ == "__main__":
  wpilib.run(MyRobot)
