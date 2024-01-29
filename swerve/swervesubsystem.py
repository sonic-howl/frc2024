import math
from threading import Thread
from time import sleep
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

  front_left = SwerveModule(
    SwerveConstants.fl_drive_id,
    SwerveConstants.fl_turn_id,
    abs_encoder_offset_rad=SwerveConstants.fl_abs_encoder_offset_rad,
    chassis_angular_offset=SwerveConstants.fl_chassis_angular_offset,
  )
  front_right = SwerveModule(
    SwerveConstants.fr_drive_id,
    SwerveConstants.fr_turn_id,
    abs_encoder_offset_rad=SwerveConstants.fr_abs_encoder_offset_rad,
    chassis_angular_offset=SwerveConstants.fr_chassis_angular_offset,
  )
  back_left = SwerveModule(
    SwerveConstants.bl_drive_id,
    SwerveConstants.bl_turn_id,
    abs_encoder_offset_rad=SwerveConstants.bl_abs_encoder_offset_rad,
    chassis_angular_offset=SwerveConstants.bl_chassis_angular_offset,
  )
  back_right = SwerveModule(
    SwerveConstants.br_drive_id,
    SwerveConstants.br_turn_id,
    abs_encoder_offset_rad=SwerveConstants.br_abs_encoder_offset_rad,
    chassis_angular_offset=SwerveConstants.br_chassis_angular_offset,
  )

  odometer = SwerveDrive4Odometry(
    SwerveConstants.kDriveKinematics,
    Rotation2d(),
    (
      front_left.getPosition(),
      front_right.getPosition(),
      back_left.getPosition(),
      back_right.getPosition(),
    ),
  )

  def __init__(self) -> None:
    super().__init__()

    self.gyro = (
      AHRS(
        wpilib.SerialPort.Port.kUSB,
        AHRS.SerialDataType.kProcessedData,
        int(1 / RobotConstants.period),
      )
      if RobotConstants.navxPort == RobotConstants.NavXPort.kUSB
      else AHRS(
        wpilib.SPI.Port.kMXP,
        int(1 / RobotConstants.period),
      )
    )

    def resetGyro():
      """reset gyro after it's calibration of 1s"""
      sleep(1)
      self.resetGyro()

    Thread(target=resetGyro).start()

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

    if not RobotConstants.isSimulation:
      self.field = Field2d()
      SmartDashboard.putData("Field", self.field)

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
    # self.gyro.zeroYaw()
    self.gyro.reset()

  def reset_motor_positions(self):
    self.front_left.resetEncoders()
    self.front_right.resetEncoders()
    self.back_left.resetEncoders()
    self.back_right.resetEncoders()

  def resetOdometer(self, pose: Pose2d = Pose2d()):
    self.odometer.resetPosition(
      self.getRotation2d(),
      pose,
      self.front_left.getPosition(),
      self.front_right.getPosition(),
      self.back_left.getPosition(),
      self.back_right.getPosition(),
    )

  def periodic(self) -> None:
    # TODO print gyro angle, robot pose on dashboard

    if not RobotConstants.isSimulation:
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
    x = utils.utils.dz(self.controller.getForward()) * speed_scale
    y = utils.utils.dz(self.controller.getStrafe()) * speed_scale
    z = self.controller.getTurn() * speed_scale
    # z = self.zLimiter.calculate(z)
    z = utils.utils.calcAxisSpeedWithCurvatureAndDeadzone(z)
    # convert values to meters per second and apply rate limiters
    x *= SwerveConstants.kDriveMaxMetersPerSecond
    # x = self.xLimiter.calculate(x)

    y *= SwerveConstants.kDriveMaxMetersPerSecond
    # y = self.yLimiter.calculate(y)

    z = self.zLimiter.calculate(z)

    if self.get_field_oriented():
      chassisSpeeds = ChassisSpeeds.fromFieldRelativeSpeeds(
          x,
          y,
          z,
          self.swerveSubsystem.getRotation2d(),
            )
    else:
      chassisSpeeds = ChassisSpeeds(
        x,
        y,
        z,
          )

    #if RobotConstants.isSimulation:
      #self.swerveSubsystem.simChassisSpeeds = chassisSpeeds

    swerveModuleStates = SwerveSubsystem.toSwerveModuleStatesForecast(
      chassisSpeeds
        )
    self.swerveSubsystem.setModuleStates(swerveModuleStates)

  def stop(self) -> None:
    self.front_left.stop()
    self.front_right.stop()
    self.back_left.stop()
    self.back_right.stop()

    if RobotConstants.isSimulation:
      self.simChassisSpeeds = None

  def setX(self) -> None:
    self.front_left.setDesiredState(
      SwerveModuleState(0, Rotation2d.fromDegrees(-45)), True
    )
    self.front_right.setDesiredState(
      SwerveModuleState(0, Rotation2d.fromDegrees(45)), True
    )
    self.back_left.setDesiredState(
      SwerveModuleState(0, Rotation2d.fromDegrees(45)), True
    )
    self.back_right.setDesiredState(
      SwerveModuleState(0, Rotation2d.fromDegrees(-45)), True
    )

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
