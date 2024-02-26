import ntcore
import wpilib
import wpimath
from cscore import CameraServer
from cscore import VideoMode

import dashboard
import driveteam
import swerve.swervesubsystem
import utils.utils

from constants.RobotConstants import RobotConstants
from constants.ntconstants import VisionTable

class MyRobot(wpilib.TimedRobot):

  def __init__(self):
    wpilib._wpilib.TimedRobot.__init__(self)
    
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

    # pose info from computer vision
    self.vx = 0.0
    self.vy = 0.0
    self.vr = 0.0
    self.ts = 0
    self.vision_pose = ntcore.TimestampedFloat()

    self.driveteam = driveteam.DriveTeam()
    self.drivebase = swerve.swervesubsystem.SwerveSubsystem()


  def getInputs(self):
    self.strafe = self.driveteam.strafe_command()
    self.turn = self.driveteam.turn_command()
    self.drive = self.driveteam.drive_command()
    #self.winch = self.driveteam.get_winch_command()
    #self.hookextend = self.driveteam.get_hook_extension_command()
    #self.hookretract = self.driveteam.get_hook_retract_command()
    #self.hookleft = self.driveteam.get_hook_left_command()
    #self.hookright = self.driveteam.get_hook_right_command()

    #self.aim = self.driveteam.get_aim_command()
    self.fire = self.driveteam.launch_command()
    self.unjam = self.driveteam.unjam_command()
    self.pickup = self.driveteam.pickup_command()
    self.eject = self.driveteam.eject_command()


  def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """
    # CameraServer.launch will immediately return in simulation
    #wpilib.cameraserver.CameraServer.launch()
    usbCam = CameraServer.startAutomaticCapture()
    usbCam.setVideoMode( VideoMode.PixelFormat.kMJPEG, 640, 480, 30 )

    RobotConstants.period = self.getPeriod()

    # Set up network tables
    self.network_table = ntcore.NetworkTableInstance.getDefault()
    self.vision_table = self.network_table.getTable( VisionTable.name )
    self.bot_pose_sub = self.vision_table.getFloatArrayTopic( VisionTable.bot_pose ).subscribe( [0.0, 0.0, 0.0] )

  def robotPeriodic(self):
    """
    Periodic code for all modes should go here.
        
    This function is called each time a new packet is received from the driver station.
    """
    # Check on network tables 
    # Location from computer vision, perform sanity check 
    self.vision_pose = self.bot_pose_sub.getAtomic()

    # Check if new pose was published
    if self.vision_pose.time != self.ts:

      # TBD run additional checks for movement and range, possibly average out the pose
      self.vx = self.vision_pose.value[0]
      self.vy = self.vision_pose.value[1]
      self.vr = self.vision_pose.value[2]

      self.drivebase.resetOdometer( wpimath.geometry.Pose2d( self.vx, self.vy, self.vr ) )

      self.ts = self.vision_pose.time
    
  def disabledInit(self):
    """
    This function is called each and every time disabled is entered from another mode
    """
  
  def disabledPeriodic(self):
    # Execute commands on the subsystems to allow periodic monitoring.
    self.drivebase.stop()

  def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""

  def autonomousPeriodic(self):
    # TBD Autonomous commands
    self.drivebase.stop()

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
