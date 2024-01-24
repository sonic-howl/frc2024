from enum import Enum


class RobotConstants:
  # !
  maxSpeed = 1
  scale_speed = 1
  rotationScale = 0.5
  rotationCurvature = 2.0
  rotationDeadzone = 0.075

  isSimulation = False

  period = 0.02

  controller_deadzone = 0.05
  pilot_controller_id = 0
  operator_controller_id = 1

  frame_width = 27
  frame_length = 26

  light_strip_pwm_port = 1

  class NavXPort(Enum):
    kUSB = 1
    kSPI = 2

  navxPort = NavXPort.kUSB
