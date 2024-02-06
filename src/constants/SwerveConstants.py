import math

from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics

from constants.RobotConstants import RobotConstants


class FalconConstants:
  kMotorFreeSpeedRPM = 6380
  kUnitsPerRotation = 2048


class SwerveConstants:
  swerveDashboardName = "Swerve Dashboard"

  # to change the robot orientation (which way is front)
  # or if wheels are in the wrong orientation when rotating but fine when moving forward, change these
  kDriveKinematics = SwerveDrive4Kinematics(
    Translation2d(RobotConstants.frame_width / 2, RobotConstants.frame_length / 2),
    Translation2d(RobotConstants.frame_width / 2, -RobotConstants.frame_length / 2),
    Translation2d(-RobotConstants.frame_width / 2, -RobotConstants.frame_length / 2),
    Translation2d(-RobotConstants.frame_width / 2, RobotConstants.frame_length / 2),
  )

  fl_drive_id = 2
  fl_turn_id = 3
  fl_abs_encoder_offset_rad = 0.0 #0.8371254
  fl_chassis_angular_offset = -math.pi / 2
 

  fr_drive_id = 4
  fr_turn_id = 5
  fr_abs_encoder_offset_rad = 0.0 #0.1121867
  fr_chassis_angular_offset = 0

  bl_drive_id = 6
  bl_turn_id = 7
  bl_abs_encoder_offset_rad = 0.0 #0.4243934
  bl_chassis_angular_offset = math.pi

  br_drive_id = 8
  br_turn_id = 9
  br_abs_encoder_offset_rad = 0.0 #0.0935666
  br_chassis_angular_offset = math.pi / 2

  kPTurning = 1
  # kPTurning = 0.4
  kITurning = 0
  kDTurning = 0

  # TODO calibrate
  kDriveMaxMetersPerSecond = 5.15
  kDriveMaxAccelerationMetersPerSecond = 3.0
  kDriveMaxTurnMetersPerSecond = 8.0
  kDriveMaxTurnAccelerationMetersPerSecond = 5
  kDriveXLimit = 5
  kDriveYLimit = 5
  kDriveZLimit = 4

  kPRobotTurn = 1
  kIRobotTurn = 0.1
  kDRobotTurn = 0.005

  inches_to_meters = 39.37

  kDrivingMotorReduction = 5.08

  kWheelDiameterMeters = 3 / inches_to_meters
  kWheelCircumferenceMeters = kWheelDiameterMeters * math.pi
  # kWheelRotationsPerMeter = 1 / kWheelCircumference
  kEncoderPulsesPerRevolution = (
    kDrivingMotorReduction * FalconConstants.kUnitsPerRotation
  )  # manually measured as 10532
  kEncoderPositionPerMeter = kEncoderPulsesPerRevolution / kWheelCircumferenceMeters

  # print("kEncoderPositionPerMeter", kEncoderPositionPerMeter)

  kDriveWheelFreeSpeedRps = (
    FalconConstants.kMotorFreeSpeedRPM * kWheelCircumferenceMeters
  ) / kDrivingMotorReduction

  # print("kDriveWheelFreeSpeedRps", kDriveWheelFreeSpeedRps)

  # kDrivingEncoderPositionFactor = (
  #     kWheelCircumferenceMeters
  # ) / kDrivingMotorReduction  # meters per encoder position

  # kDrivingEncoderPositionFactor = (
  #     kWheelCircumferenceMeters * kDrivingMotorReduction
  # ) / ((FalconConstants.kMotorFreeSpeedRPM / 60) * kEncoderPulsesPerRevolution)

  # kDrivingEncoderVelocityFactor = (
  #     kWheelCircumferenceMeters / kDrivingMotorReduction
  # ) / 60.0  # meters per second
  # # kDrivingEncoderVelocityFactor = 3.135

  # calibrated_vs = (vs / kEncoderPositionPerMeter) * 10 # multiplied by 10 to get m/100ms to m/s
  # vs = (calibrated_vs / 10) * kEncoderPositionPerMeter

  # TODO tune this once it is on the ground
  kMaxMeasuredVelocityEncoderUnits = 18000
  typical_drive_velocity = 0.8
  kFDriving = (typical_drive_velocity * 1023) / kMaxMeasuredVelocityEncoderUnits
