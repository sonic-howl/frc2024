import math
from typing import Callable, Set

from commands2 import Command, Subsystem
from wpimath.controller import PIDController
from wpimath.filter import SlewRateLimiter
from wpimath.kinematics import ChassisSpeeds

from constants.RobotConstants import RobotConstants
from constants.SwerveConstants import SwerveConstants
from controllers.pilot import PilotController
from frc2024.swerve.swervesubsystem import SwerveSubsystem
from utils.utils import calcAxisSpeedWithCurvatureAndDeadzone, dz


class SwerveCommand(Command):
  def __init__(
    self,
    swerveSubsystem: SwerveSubsystem,
    controller: PilotController,
    getFieldOriented: Callable[[], bool],
  ) -> None:
    super().__init__()

    self.swerveSubsystem = swerveSubsystem

    self.controller = controller
    self.get_field_oriented = getFieldOriented

    # self.xLimiter = SlewRateLimiter(
    #     SwerveConstants.kDriveXLimit, -SwerveConstants.kDriveXLimit
    # )
    # self.yLimiter = SlewRateLimiter(SwerveConstants.kDriveYLimit)
    self.zLimiter = SlewRateLimiter(SwerveConstants.kDriveZLimit)

  def getRequirements(self) -> Set[Subsystem]:
    return {self.swerveSubsystem}

  def initialize(self) -> None:
    print("SwerveCommand initialized")
    pass

  def execute(self) -> None:
    if not self.controller.isConnected():
      return

    speed_scale = self.controller.getSpeed()

    x = dz(self.controller.getForward()) * speed_scale
    y = dz(self.controller.getStrafe()) * speed_scale

    z = 0.0

    pov = self.controller.getRotateToAngle()
    if pov != -1:
      # TODO calibrate this PID controller
      z = self.swerveSubsystem.theta_pid.calculate(
        math.radians(self.swerveSubsystem.getAngle()),
        math.radians(360 - pov),
      )
      # print("pov debug: ", pov, self.swerveSubsystem.getAngle(), z)
    else:
      z = self.controller.getTurn() * speed_scale
      # z = self.zLimiter.calculate(z)
      z = calcAxisSpeedWithCurvatureAndDeadzone(z)

    magnitude = abs(x) + abs(y) + abs(z)
    if dz(magnitude) > 0:
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

      if RobotConstants.isSimulation:
        self.swerveSubsystem.simChassisSpeeds = chassisSpeeds

      swerveModuleStates = SwerveSubsystem.toSwerveModuleStatesForecast(chassisSpeeds)
      self.swerveSubsystem.setModuleStates(swerveModuleStates)
    else:
      if RobotConstants.isSimulation:
        self.swerveSubsystem.simChassisSpeeds = None

      self.swerveSubsystem.stop()

  def end(self, interrupted: bool) -> None:
    print("SwerveCommand ended")
    self.swerveSubsystem.stop()

  def isFinished(self) -> bool:
    return False
