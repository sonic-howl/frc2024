import math
from typing import Tuple

import wpilib
from navx import AHRS
from wpimath.controller import ProfiledPIDControllerRadians
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import (
  ChassisSpeeds,
  SwerveDrive4Kinematics,
  SwerveDrive4Odometry,
  SwerveModuleState,
)
from wpimath.trajectory import TrapezoidProfileRadians

import utils.utils
from constants.RobotConstants import RobotConstants
from constants.SwerveConstants import SwerveConstants
from swerve.SwerveModule import SwerveModule


class SwerveSubsystem:
  simChassisSpeeds: ChassisSpeeds | None = None
  """Meant for simulation only"""
  swerveAutoStartPose: Pose2d | None = None
  """Meant for simulation only"""

  def __init__(self) -> None:
    self.field_oriented = True
    self.gyro = AHRS(
      wpilib.SerialPort.Port.kMXP,
      AHRS.SerialDataType.kProcessedData,
      int(1 / RobotConstants.period),
    )
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

    self.gyroCalibrated = False

    self.odometerGyroOffset = Rotation2d()

  def getAngle(self) -> float:
    return -self.gyro.getYaw()

  def getRotation2d(self):
    return Rotation2d.fromDegrees(self.getAngle())

  def getPose(self) -> Pose2d:
    return self.odometer.getPose()

  def resetGyro(self):
    # self.gyro.zeroYaw()
    self.gyro.reset()

  def isCalibrated(self):
    return self.gyroCalibrated

  def reset_motor_positions(self):
    self.front_left.resetEncoders()
    self.front_right.resetEncoders()
    self.back_left.resetEncoders()
    self.back_right.resetEncoders()

  def resetOdometer(self, pose: Pose2d = Pose2d()):
    self.odometerGyroOffset = pose.rotation() - self.getRotation2d()

    self.odometer.resetPosition(
      self.getRotation2d(),
      [
        self.front_left.getPosition(),
        self.front_right.getPosition(),
        self.back_left.getPosition(),
        self.back_right.getPosition(),
      ],
      pose,
    )
    # potentially call gyro.setAngleAdjustment to align gyro with odometry (not necessary if we only use odometry)

  def periodic(self) -> None:
    (
      self.odometer.update(
        self.getRotation2d(),
        (
          self.front_left.getPosition(),
          self.front_right.getPosition(),
          self.back_left.getPosition(),
          self.back_right.getPosition(),
        ),
      )
    )

    if self.isCalibrated():
      if self.gyro.isCalibrating():
        self.gyroCalibrated = False
    elif not self.gyro.isCalibrating():
      self.resetGyro()
      self.gyroCalibrated = True

  def toggleFieldOriented(self):
    self.field_oriented = not self.field_oriented

  def setvelocity(self, drive: float, strafe: float, rotate: float):
    self.periodic()
    speed_scale = 1.0
    x = utils.utils.dz(drive) * speed_scale
    y = utils.utils.dz(strafe) * speed_scale
    z = utils.utils.dz(rotate) * speed_scale
    z = utils.utils.calcAxisSpeedWithCurvatureAndDeadzone(z)
    # convert values to meters per second and apply rate limiters
    x *= SwerveConstants.kDriveMaxMetersPerSecond

    y *= SwerveConstants.kDriveMaxMetersPerSecond

    if self.field_oriented:
      chassisSpeeds = ChassisSpeeds.fromFieldRelativeSpeeds(
        x,
        y,
        z,
        self.getRotation2d()
        + self.odometerGyroOffset,  # Adding the odometry gyro offset at init to correct for the 180 degree difference
      )
    else:
      chassisSpeeds = ChassisSpeeds(
        x,
        y,
        z,
      )

    swerveModuleStates = SwerveSubsystem.toSwerveModuleStatesForecast(chassisSpeeds)
    self.setModuleStates(swerveModuleStates)

  def stop(self) -> None:
    self.periodic()
    self.front_left.stop()
    self.front_right.stop()
    self.back_left.stop()
    self.back_right.stop()

    if not wpilib.RobotBase.isReal():
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

  def moveToPose(self, pose: Pose2d):
    currentPose = self.getPose()
    x = currentPose.X()
    y = currentPose.Y()
    rotation = currentPose.rotation().radians()

    errorX = pose.X() - x
    errorY = pose.Y() - y
    errorR = pose.rotation().radians() - rotation

    errorR = math.fmod(errorR, 2.0 * math.pi)
    if errorR > math.pi:
      errorR = errorR - (2.0 * math.pi)
    elif errorR < -math.pi / 2.0:
      errorR = errorR + (2.0 * math.pi)

    KpX = 1
    KpY = 1
    KpRotation = 1

    commandX = errorX * KpX
    commandY = errorY * KpY
    commandRotation = errorR * KpRotation

    commandX = utils.utils.limiter(commandX, -0.5, 0.5)
    commandY = utils.utils.limiter(commandY, -0.5, 0.5)
    commandRotation = utils.utils.limiter(commandRotation, -1, 1)
    # Set to .7 to prevent skidding
    self.field_oriented = True

    self.setvelocity(commandX, commandY, commandRotation)
