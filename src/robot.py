import math

import ntcore
import wpilib
import wpilib.deployinfo
import wpimath.geometry
from commands2 import CommandScheduler, InstantCommand, Subsystem
from pathplannerlib.auto import (
  AutoBuilder,
  HolonomicPathFollowerConfig,
  NamedCommands,
  ReplanningConfig,
)
from pathplannerlib.config import PIDConstants
from wpilib import DriverStation, Field2d, SmartDashboard

import drivestation
import driveteam
import launcher
import swerve.swervesubsystem
import utils.utils
from AutoSelector import AutoSelector
from constants.networktables import PoseInfo
from constants.RobotConstants import RobotConstants
from constants.SwerveConstants import SwerveConstants
from shuffleboard import addDeployArtifacts


class Robot(wpilib.TimedRobot):
  def __init__(self):
    super().__init__()

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

  def configureAuto(self):
    NamedCommands.registerCommand(
      "shoot", InstantCommand(lambda: print("shoot tested!!!"))
    )
    NamedCommands.registerCommand(
      "pickup", InstantCommand(lambda: print("pickup tested!!!"))
    )

    AutoBuilder.configureHolonomic(
      self.drivebase.getPose,
      self.drivebase.resetOdometer,
      self.drivebase.getChassisSpeeds,
      self.drivebase.setChassisSpeeds,
      HolonomicPathFollowerConfig(
        PIDConstants(
          SwerveConstants.kPRobotStrafe,
          SwerveConstants.kIRobotStrafe,
          SwerveConstants.kDRobotStrafe,
        ),
        PIDConstants(
          SwerveConstants.kPRobotTurn,
          SwerveConstants.kIRobotTurn,
          SwerveConstants.kDRobotTurn,
        ),
        SwerveConstants.kDriveMaxMetersPerSecond,
        RobotConstants.frame_width / 2,
        ReplanningConfig(enableDynamicReplanning=False),
        RobotConstants.period,
      ),
      should_flip_path=self.isRedAlliance,
      drive_subsystem=Subsystem(),
    )

  def isRedAlliance(self):
    return DriverStation.getAlliance() == DriverStation.Alliance.kRed

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
    self.init_NT()

    self.configureAuto()
    self.autoSelector = AutoSelector()

    self.commandScheduler = CommandScheduler()

    # Add 2D Field to SmartDashboard
    self.field = Field2d()
    SmartDashboard.putData("Field", self.field)

    # Add the deploy artifacts to the shuffleboard
    addDeployArtifacts()

  def robotPeriodic(self):
    self.commandScheduler.run()

  def disabledPeriodic(self):
    self.drivebase.stop()

    self.setOutputs()

  def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""
    # Check only once during autonomous initialization for setting initial pose
    (self.startingPose, self.autoSelected) = self.autoSelector.getSelectedAuto()

    self.drivebase.resetOdometer(
      self.startingPose if self.startingPose else wpimath.geometry.Pose2d()
    )
    self.commandScheduler.schedule(self.autoSelected)

  def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""
    self.drivebase.stop()

    self.setOutputs()

  def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""
    self.commandScheduler.cancel(self.autoSelected)

  def teleopPeriodic(self):
    """This function is called periodically during teleoperated mode."""
    self.getInputs()
    drivestation.setDBLED("0", self.unjam)
    drivestation.setDBLED("1", self.eject)

    wpilib.SmartDashboard.putString("DB/String 0", str(self.drivebase.getRotation2d()))
    # drivestation.light_2(self.fire)
    # drivestation.light_3(self.pickup)

    # drive base
    if self.togglefieldoriented:
      self.drivebase.toggleFieldOriented()

    magnitude = abs(self.strafe) + abs(self.drive) + abs(self.turn)
    if utils.utils.dz(magnitude) > 0:
      self.drivebase.setvelocity(self.drive, self.strafe, self.turn)
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
