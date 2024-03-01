import math

import ntcore
import wpilib
import wpilib.deployinfo
import wpimath.geometry
from wpilib import Field2d, SmartDashboard

import constants.FieldConstants as FieldConstants
import drivestation
import driveteam
import launcher
import swerve.swervesubsystem
import utils.utils
from constants.networktables import PoseInfo
from constants.RobotConstants import RobotConstants
from shuffleboard import addDeployArtifacts


class MyRobot(wpilib.TimedRobot):
  def __init__(self):
    wpilib._wpilib.TimedRobot.__init__(self)

    self.pilots = driveteam.DriveTeam()
    self.drivebase = swerve.swervesubsystem.SwerveSubsystem()
    self.launcher = launcher.Launchers()

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

  def init_NT(self):
    """
    This function initializes network tables for the robot
    """
    self.network_table = ntcore.NetworkTableInstance.getDefault()
    self.pose_table = self.network_table.getTable(PoseInfo.name)
    # self.odometry_pose_pub = self.pose_table.getFloatArrayTopic(
    #   PoseInfo.odometry_pose
    # ).publish()
    self.odometry_x_pub = self.pose_table.getFloatTopic(PoseInfo.odometry_x).publish()
    self.odometry_y_pub = self.pose_table.getFloatTopic(PoseInfo.odometry_y).publish()
    self.odometry_r_pub = self.pose_table.getFloatTopic(PoseInfo.odometry_r).publish()
    self.gyro_pub = self.pose_table.getFloatTopic(PoseInfo.gyro_angle).publish()

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

    self.togglefieldoriented = self.pilots.get_view_command()

    self.moveToAmp = self.pilots.get_move_to_amp_command()
    self.moveToSpeaker = self.pilots.get_move_to_speaker_command()
    self.moveToPickupLeft = self.pilots.get_move_to_pickup_left_command()
    self.moveToPickupRight = self.pilots.get_move_to_pickup_right_command()

  def setOutputs(self):
    # Robot Pose
    odometry_pose = self.drivebase.getPose()
    # self.odometry_pose_pub.set(
    #   [odometry_pose.X(), odometry_pose.Y(), odometry_pose.rotation().degrees()]
    # )
    self.odometry_x_pub.set(odometry_pose.X())
    self.odometry_y_pub.set(odometry_pose.Y())
    self.odometry_r_pub.set(odometry_pose.rotation().degrees())
    self.gyro_pub.set(self.drivebase.getAngle())
    # Update Field2D Robot Pose
    self.field.setRobotPose(self.drivebase.getPose())

  def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """
    # Sendable Chooser
    self.defaultAuto = "Default Auto"
    self.blueLeft = "Blue Left"
    self.blueMiddle = "Blue Middle"
    self.blueRight = "Blue Right"
    self.redRight = "Red Right"
    self.redMiddle = "Red Middle"
    self.redLeft = "Red Left"

    self.init_NT()

    self.chooser = wpilib.SendableChooser()

    self.chooser.setDefaultOption("Default Auto", self.defaultAuto)
    self.chooser.addOption("Blue Left", self.blueLeft)
    self.chooser.addOption("Blue Middle", self.blueMiddle)
    self.chooser.addOption("Blue Right", self.blueRight)
    self.chooser.addOption("Red Right", self.redRight)
    self.chooser.addOption("Red Middle", self.redMiddle)
    self.chooser.addOption("Red Left", self.redLeft)
    wpilib.SmartDashboard.putData("Auto choices", self.chooser)

    # Add 2D Field to SmartDashboard
    self.field = Field2d()
    SmartDashboard.putData("Field", self.field)

    # Add the deploy artifacts to the shuffleboard
    addDeployArtifacts()

  def disabledPeriodic(self):
    self.drivebase.stop()

    self.setOutputs()

  def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""
    # Check only once during autonomous initialization for setting initial pose
    self.autoSelected = self.chooser.getSelected()

    match self.autoSelected:
      # Positions mark the autonomous start line, adjust for frame and bumpers
      case self.blueLeft:
        kX = 76.125 - RobotConstants.frame_length / 2 - RobotConstants.bumper_width
        kY = 275.42
        kRotation = math.pi
      case self.blueMiddle:
        kX = 76.125 - RobotConstants.frame_length / 2 - RobotConstants.bumper_width
        kY = 218.42
        kRotation = math.pi
      case self.blueRight:
        kX = 76.125 - RobotConstants.frame_length / 2 - RobotConstants.bumper_width
        kY = 161.42
        kRotation = math.pi
      case self.redRight:
        kX = 577.125 + RobotConstants.frame_length / 2 + RobotConstants.bumper_width
        kY = 275.42
        kRotation = 0
      case self.redMiddle:
        kX = 577.125 + RobotConstants.frame_length / 2 + RobotConstants.bumper_width
        kY = 218.42
        kRotation = 0
      case self.redLeft:
        kX = 577.125 + RobotConstants.frame_length / 2 + RobotConstants.bumper_width
        kY = 161.42
        kRotation = 0
      case _:
        kX = 0
        kY = 0
        kRotation = 0

    # Set the dashboard programmed initial pose.
    inchToM = 39.73  # Inches to metres (x / inchToM)
    if self.drivebase.isCalibrated():
      self.drivebase.resetOdometer(
        wpimath.geometry.Pose2d(kX / inchToM, kY / inchToM, kRotation)
      )
    # else the gyro is probably broken if it is still calibrating, degraded operations tbd.

  def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""
    self.drivebase.stop()

    self.setOutputs()

  def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""

  def teleopPeriodic(self):
    """This function is called periodically during teleoperated mode."""
    self.getInputs()
    drivestation.setDBLED("0", self.unjam)
    drivestation.setDBLED("1", self.eject)

    wpilib.SmartDashboard.putString("DB/String 0", str(self.drivebase.getRotation2d()))

    # drive base
    if self.togglefieldoriented:
      self.drivebase.toggleFieldOriented()

      wpilib.SmartDashboard.putString(
        "fieldOriented", str(self.drivebase.field_oriented)
      )

    magnitude = abs(self.strafe) + abs(self.drive) + abs(self.turn)
    if utils.utils.dz(magnitude) > 0:
      if (
        wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed
        and self.drivebase.field_oriented
      ):
        self.drivebase.setvelocity(-self.drive, -self.strafe, self.turn)
      else:
        self.drivebase.setvelocity(self.drive, self.strafe, self.turn)
    elif self.moveToAmp:
      if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
        self.drivebase.moveToPose(
          FieldConstants.kBlueAmpLocation.transformBy(
            wpimath.geometry.Transform2d(0, -FieldConstants.kAmpShootingRange, 0)
          )
        )
      else:
        self.drivebase.moveToPose(
          FieldConstants.kRedAmpLocation.transformBy(
            wpimath.geometry.Transform2d(0, -FieldConstants.kAmpShootingRange, 0)
          )
        )
    elif self.moveToSpeaker:
      if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
        self.drivebase.moveToPose(
          FieldConstants.kBlueSpeakerLocation.transformBy(
            wpimath.geometry.Transform2d(0, +FieldConstants.kSpeakerShootingRange, 0)
          )
        )
      else:
        self.drivebase.moveToPose(
          FieldConstants.kRedSpeakerLocation.transformBy(
            wpimath.geometry.Transform2d(0, -FieldConstants.kSpeakerShootingRange, 0)
          )
        )
    elif self.moveToPickupLeft:
      if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
        self.drivebase.moveToPose(
          FieldConstants.kBluePickupLeftLocation.transformBy(
            wpimath.geometry.Transform2d(
              FieldConstants.BluePickupOffset, wpimath.geometry.Rotation2d()
            )
          )
        )
      else:
        self.drivebase.moveToPose(
          FieldConstants.kRedPickupLeftLocation.transformBy(
            wpimath.geometry.Transform2d(
              FieldConstants.RedPickupOffset, wpimath.geometry.Rotation2d()
            )
          )
        )
    elif self.moveToPickupRight:
      if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
        self.drivebase.moveToPose(
          FieldConstants.kBluePickupRightLocation.transformBy(
            wpimath.geometry.Transform2d(
              FieldConstants.BluePickupOffset, wpimath.geometry.Rotation2d()
            )
          )
        )
      else:
        self.drivebase.moveToPose(
          FieldConstants.kRedPickupRightLocation.transformBy(
            wpimath.geometry.Transform2d(
              FieldConstants.RedPickupOffset, wpimath.geometry.Rotation2d()
            )
          )
        )
    else:
      self.drivebase.stop()

    # launcher
    if self.unjam:
      self.launcher.unjams()
    elif abs(self.aim) >= 0.05:
      self.launcher.elevate(self.aim)
    else:
      self.launcher.shoot(self.fire)

    self.setOutputs()

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
