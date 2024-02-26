import math
from typing import Tuple

import wpilib

import utils.utils
from navx import AHRS
from wpilib import Field2d, SmartDashboard
from wpimath.controller import (
  HolonomicDriveController,
  PIDController,
  ProfiledPIDControllerRadians,
)
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import (
  ChassisSpeeds,
  SwerveDrive4Kinematics,
  SwerveDrive4Odometry,
  SwerveModuleState,
)
from wpimath.trajectory import TrapezoidProfileRadians

from constants.RobotConstants import RobotConstants
from constants.SwerveConstants import SwerveConstants
from swerve.SwerveModule import SwerveModule


class SwerveSubsystem():
  simChassisSpeeds: ChassisSpeeds | None = None
  """Meant for simulation only"""
  swerveAutoStartPose: Pose2d | None = None
  """Meant for simulation only"""

  def __init__(self) -> None:
    self.front_left = SwerveModule(
      SwerveConstants.fl_drive_id,
      SwerveConstants.fl_turn_id,
      chassis_angular_offset=SwerveConstants.fl_chassis_angular_offset,
    )
    self.front_right = SwerveModule(
      SwerveConstants.fr_drive_id,
      SwerveConstants.fr_turn_id,
      chassis_angular_offset=SwerveConstants.fr_chassis_angular_offset,
    )
    self.back_left = SwerveModule(
      SwerveConstants.bl_drive_id,
      SwerveConstants.bl_turn_id,
      chassis_angular_offset=SwerveConstants.bl_chassis_angular_offset,
    )
    self.back_right = SwerveModule(
      SwerveConstants.br_drive_id,
      SwerveConstants.br_turn_id,
      chassis_angular_offset=SwerveConstants.br_chassis_angular_offset,
    )

    self.odometer = SwerveDrive4Odometry(
      SwerveConstants.kDriveKinematics,
      Rotation2d(),
      (
        self.front_left.getPosition(),
        self.front_right.getPosition(),
        self.back_left.getPosition(),
        self.back_right.getPosition(),
      ),
    )
    self.field_oriented = True
    self.gyro = (
      AHRS(
        wpilib.SerialPort.Port.kMXP,
        AHRS.SerialDataType.kProcessedData,
        int(1 / RobotConstants.period),
      )
    )

    self.theta_pid = ProfiledPIDControllerRadians(
      SwerveConstants.kPRobotTurn,
      SwerveConstants.kIRobotTurn,
      SwerveConstants.kDRobotTurn,
      TrapezoidProfileRadians.Constraints(
        SwerveConstants.kDriveMaxTurnMetersPerSecond,
        SwerveConstants.kDriveMaxTurnAccelerationMetersPerSecond,
      ),
      period=RobotConstants.period,
    )
    self.theta_pid.enableContinuousInput(0, math.tau)
    self.theta_pid.setTolerance(math.radians(3))

    self.field   = Field2d()
    self.cv_pose = self.field.getObject( "CV Pose" )
    SmartDashboard.putData("Field", self.field)
    
    self.gyro_calibrated = False
    

  def getAngle(self) -> float:
    # return self.gyro.getAngle() % 360
    # return self.gyro.getFusedHeading()
    # if RobotConstants.isSimulation:
    #  from physics import PhysicsEngine

    #  return PhysicsEngine.simGyro.getAngle()

    return -self.gyro.getYaw()

  def getRotation2d(self):
    return Rotation2d.fromDegrees(self.getAngle())

  def getPose(self) -> Pose2d:
    return self.odometer.getPose()

  def resetGyro(self):
    # TBD preferably set a yaw offset to match a given rotation.
    self.gyro.zeroYaw()
    #self.gyro.reset()

  def reset_motor_positions(self):
    self.front_left.resetEncoders()
    self.front_right.resetEncoders()
    self.back_left.resetEncoders()
    self.back_right.resetEncoders()

  def resetOdometer(self, pose: Pose2d = Pose2d()):
    self.odometer.resetPosition(
      self.getRotation2d(),
      [self.front_left.getPosition(),
      self.front_right.getPosition(),
      self.back_left.getPosition(),
      self.back_right.getPosition()],
      pose
    )

  def periodic(self) -> None:
    """
    This function should be called periodically before all commands 
    """
    # check for completion of gyro calibration
    # should take 1 second, completing during 5 second countdown in Disabled mode
    if not self.gyro_calibrated and not self.gyro.isCalibrating():
      # TBD handle starting yaw offset if not always aligned with field zero.
      self.gyro.zeroYaw()
      self.gyro_calibrated = True
    # TODO print gyro angle, robot pose on dashboard

    #self.field.setRobotPose( Pose2d( self.vx, self.vy, self.vr ) )
    self.field.setRobotPose(self.getPose())

    self.odometer.update(
      self.getRotation2d(),
      (
      self.front_left.getPosition(),
      self.front_right.getPosition(),
      self.back_left.getPosition(),
      self.back_right.getPosition()
      )
    )

  def setvelocity(self, drive: float, strafe: float, rotate: float):
    self.periodic()
    speed_scale = 1.0
    x = utils.utils.dz(drive) * speed_scale
    y = utils.utils.dz(strafe) * speed_scale
    z = utils.utils.dz(rotate) * speed_scale
    # z = self.zLimiter.calculate(z)
    z = utils.utils.calcAxisSpeedWithCurvatureAndDeadzone(z)
    # convert values to meters per second and apply rate limiters
    x *= SwerveConstants.kDriveMaxMetersPerSecond
    # x = self.xLimiter.calculate(x)

    y *= SwerveConstants.kDriveMaxMetersPerSecond
    # y = self.yLimiter.calculate(y)

    # z = self.zLimiter.calculate(z)

    if self.field_oriented:
      chassisSpeeds = ChassisSpeeds.fromFieldRelativeSpeeds(
          x,
          y,
          z,
          self.getRotation2d(),
            )
    else:
      chassisSpeeds = ChassisSpeeds(
        x,
        y,
        z,
      )

    #if RobotConstants.isSimulation:
      #self.simChassisSpeeds = chassisSpeeds

    swerveModuleStates = SwerveSubsystem.toSwerveModuleStatesForecast(
      chassisSpeeds
        )
    self.setModuleStates(swerveModuleStates)

  def stop(self) -> None:
    self.periodic()
    self.front_left.stop()
    self.front_right.stop()
    self.back_left.stop()
    self.back_right.stop()

    if RobotConstants.isSimulation:
      self.simChassisSpeeds = None

  @staticmethod
  def toSwerveModuleStatesForecast(chassisSpeeds: ChassisSpeeds):
    """
    Forecast the swerve module states based on the chassis speeds and the period rather than sending the current chassis speeds.
    This helps to keep the robot moving in a straight line while spinning.

    Thanks to 254: https://www.chiefdelphi.com/t/whitepaper-swerve-drive-skew-and-second-order-kinematics/416964/5
    """

    robotPoseVel = Pose2d(
      chassisSpeeds.vx * RobotConstants.period,
      chassisSpeeds.vy * RobotConstants.period,
      Rotation2d(chassisSpeeds.omega * RobotConstants.period),
    )
    twistVel = Pose2d().log(robotPoseVel)
    updatedChassisSpeeds = ChassisSpeeds(
      twistVel.dx / RobotConstants.period,
      twistVel.dy / RobotConstants.period,
      twistVel.dtheta / RobotConstants.period,
    )

    return SwerveConstants.kDriveKinematics.toSwerveModuleStates(updatedChassisSpeeds)

  def setModuleStates(
    self,
    states: Tuple[
      SwerveModuleState, SwerveModuleState, SwerveModuleState, SwerveModuleState
    ],
    isClosedLoop=False,
  ) -> None:
    fl, fr, bl, br = SwerveDrive4Kinematics.desaturateWheelSpeeds(
      states, SwerveConstants.kDriveMaxMetersPerSecond
    )
    self.front_left.setDesiredState(fl, isClosedLoop=isClosedLoop)
    self.front_right.setDesiredState(fr, isClosedLoop=isClosedLoop)
    self.back_right.setDesiredState(bl, isClosedLoop=isClosedLoop)
    self.back_left.setDesiredState(br, isClosedLoop=isClosedLoop)