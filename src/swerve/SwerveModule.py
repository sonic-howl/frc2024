import math

import phoenix5
import rev
from ntcore import NetworkTableInstance
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState

from constants.RobotConstants import RobotConstants
from constants.SwerveConstants import SwerveConstants


def scaleSpeed(speed: float) -> float:
  speed *= RobotConstants.scale_speed
  if speed > RobotConstants.maxSpeed:
    speed = RobotConstants.maxSpeed
  elif speed < -RobotConstants.maxSpeed:
    speed = -RobotConstants.maxSpeed
  return speed


class SwerveModule:
  def __init__(
    self,
    drive_motor_id: int,
    turn_motor_id: int,
    chassis_angular_offset=0.0,
    abs_encoder_reversed=True,
    turn_motor_reversed=False,
  ) -> None:
    self.chassis_angular_offset = chassis_angular_offset

    # set angle offset
    self.abs_encoder_reversed = abs_encoder_reversed

    self.turn_motor_id = turn_motor_id

    # create motors
    # drive motor
    self.drive_motor = phoenix5.WPI_TalonFX(drive_motor_id)
    # talonfx_configs = configs.TalonFXConfiguration()

    # ----
    self.drive_motor.configPeakOutputReverse(-RobotConstants.maxSpeed)
    self.drive_motor.configPeakOutputForward(RobotConstants.maxSpeed)
    self.drive_motor.configClosedLoopPeakOutput(0, RobotConstants.maxSpeed)
    self.drive_motor.configFactoryDefault()
    self.drive_motor.setNeutralMode(phoenix5.NeutralMode.Brake)
    self.drive_motor.configStatorCurrentLimit(
      phoenix5.StatorCurrentLimitConfiguration(True, 25, 30, 0.5)
    )
    self.drive_motor.configSupplyCurrentLimit(
      phoenix5.SupplyCurrentLimitConfiguration(True, 30, 35, 0.5)
    )
    self.drive_motor.configOpenloopRamp(0.25)
    self.drive_motor.setSelectedSensorPosition(0)
    # self.drive_motor.configSelectedFeedbackCoefficient(
    #     1 / SwerveConstants.kDrivingEncoderPositionFactor
    # )
    self.drive_motor.config_kP(0, 0)
    self.drive_motor.config_kI(0, 0)
    self.drive_motor.config_kD(0, 0)
    # self.drive_motor.config_kF(0, 1)
    self.drive_motor.config_kF(0, SwerveConstants.kFDriving)
    # self.drive_motor.

    # turn motor
    self.turn_motor = rev.CANSparkMax(
      turn_motor_id, rev.CANSparkLowLevel.MotorType.kBrushless
    )
    # ?
    self.turn_motor.restoreFactoryDefaults()
    self.turn_motor.setInverted(turn_motor_reversed)
    self.turn_motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
    # self.turn_motor.setOpenLoopRampRate(200 / 1000)  # ms
    self.turn_motor.setSmartCurrentLimit(20)
    self.turn_motor.setSecondaryCurrentLimit(20)

    # create encoders
    self.turn_encoder = self.turn_motor.getAbsoluteEncoder(
      rev.SparkMaxAbsoluteEncoder.Type.kDutyCycle
    )
    self.turn_encoder.setPositionConversionFactor(math.pi * 2)  # radians
    self.turn_encoder.setVelocityConversionFactor(
      (math.pi * 2) / 60
    )  # radians per second
    self.turn_encoder.setInverted(abs_encoder_reversed)

    # We are not using the built in PID controller, but this is where the config would go...
    # self. #...
    self.turn_pid = self.turn_motor.getPIDController()
    self.turn_pid.setFeedbackDevice(self.turn_encoder)
    self.turn_pid.setP(SwerveConstants.kPTurning)
    self.turn_pid.setI(SwerveConstants.kITurning)
    self.turn_pid.setD(SwerveConstants.kDTurning)
    self.turn_pid.setPositionPIDWrappingEnabled(True)
    self.turn_pid.setPositionPIDWrappingMinInput(0)
    self.turn_pid.setPositionPIDWrappingMaxInput(math.pi * 2)
    self.turn_pid.setOutputRange(-1, 1)

    self.turn_motor.burnFlash()

    self.resetEncoders()

    self.initNetworkTables()

    self.lastDesiresState = self.getState()

  def initNetworkTables(self):
    network_table_instance = NetworkTableInstance.getDefault()
    self.swerve_dashboard = network_table_instance.getTable(
      SwerveConstants.swerveDashboardName
    )
    self.angle_topic_pub = self.swerve_dashboard.getDoubleTopic(
      f"module angle {self.turn_motor_id}"
    ).publish()
    self.drive_speed_topic_pub = self.swerve_dashboard.getDoubleTopic(
      f"module drive speed {self.turn_motor_id}"
    ).publish()
    self.set_point_topic_pub = self.swerve_dashboard.getDoubleTopic(
      f"module set point angle {self.turn_motor_id}"
    ).publish()

    # self.turn_kP_topic = self.swerve_dashboard.getFloatTopic(
    #     f"module kP {self.turn_motor_id}"
    # )
    # self.turn_kP = self.turn_kP_topic.publish()
    # self.turn_kP.setDefault(SwerveConstants.kPTurning)
    # self.turn_kP_sub = self.turn_kP_topic.subscribe(0)

    # self.turn_kI_topic = self.swerve_dashboard.getFloatTopic(
    #     f"module kI {self.turn_motor_id}"
    # )
    # self.turn_kI = self.turn_kI_topic.publish()
    # self.turn_kI.set(SwerveConstants.kITurning)
    # self.turn_kI_sub = self.turn_kI_topic.subscribe(0)

    # self.turn_kD_topic = self.swerve_dashboard.getFloatTopic(
    #     f"module kD {self.turn_motor_id}"
    # )
    # self.turn_kD = self.turn_kD_topic.publish()
    # self.turn_kD.set(SwerveConstants.kDTurning)
    # self.turn_kD_sub = self.turn_kD_topic.subscribe(0)

  def resetEncoders(self) -> None:
    self.drive_motor.setSelectedSensorPosition(0)

  def getRotation(self) -> Rotation2d:
    return Rotation2d(self.turn_encoder.getPosition() - self.chassis_angular_offset)

  def getPosition(self) -> SwerveModulePosition:
    return SwerveModulePosition(
      # distance=sensor_pos / SwerveConstants.kEncoderPositionPerMeter,
      distance=self.drive_motor.getSelectedSensorPosition()
      / SwerveConstants.kEncoderPositionPerMeter,
      # distance=self.drive_motor.getSelectedSensorPosition()
      # / SwerveConstants.kEncoderPositionPerMeter,
      angle=self.getRotation(),
    )

  def getState(self) -> SwerveModuleState:
    return SwerveModuleState(
      speed=self.drive_motor.getSelectedSensorVelocity(),
      angle=self.getRotation(),
    )

  def setDesiredState(
    self, state: SwerveModuleState, force_angle=False, isClosedLoop=False
  ) -> None:
    if not force_angle and abs(state.speed) < 0.01:
      self.stop()
      return

    state.angle += Rotation2d(self.chassis_angular_offset)

    current_angle = self.turn_encoder.getPosition()

    # optimize AFTER adding the chassis angular offset
    state = SwerveModuleState.optimize(state, Rotation2d(current_angle))

    # # TODO make a drive velocity PID instead of scaling it this way
    # drive_speed = state.speed / SwerveConstants.kDriveMaxMetersPerSecond
    # drive_speed = scale_speed(drive_speed)
    # self.drive_motor.set(drive_speed)

    drive_speed = state.speed / 10 * SwerveConstants.kEncoderPositionPerMeter

    # print(f"state speed: {state.speed}, drive speed: {drive_speed}")

    self.drive_motor.set(
      phoenix5.ControlMode.Velocity,
      drive_speed,
    )

    set_point = state.angle.radians()

    # turn_speed = self.turn_pid.calculate(current_angle, set_point)
    # turn_speed = scale_speed(turn_speed)

    self.angle_topic_pub.set(math.degrees(current_angle))
    self.drive_speed_topic_pub.set(state.speed)
    self.set_point_topic_pub.set(math.degrees(set_point - self.chassis_angular_offset))

    # self.turn_motor.set(turn_speed)
    self.turn_pid.setReference(set_point, rev.CANSparkMax.ControlType.kPosition)

    self.lastDesiresState = state

  def stop(self) -> None:
    self.drive_motor.stopMotor()
    self.turn_motor.stopMotor()
