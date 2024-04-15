from threading import Thread

from constants.RobotConstants import RobotConstants


def printAsync(*args, **kwargs) -> None:
  """print in a new thread"""
  Thread(target=print, args=args, kwargs=kwargs).start()


def limiter(value, min, max):
  if value > max:
    value = max
  elif value < min:
    value = min
  return value


def sgn(x: float) -> float:
  """return the sign of x"""
  return -1 if x < 0 else 1


def dz(x: float, dz=RobotConstants.controller_deadzone):
  return x if abs(x) > dz else 0


def calcAxisSpeedWithCurvatureAndDeadzone(
  x: float,
  c=RobotConstants.rotationCurvature,
  b=RobotConstants.rotationDeadzone,
  dz=RobotConstants.controller_deadzone,
  scale_speed=RobotConstants.rotationScale,
):
  """
  Calculate the speed of the axis with curvature and deadzone

  Desmos graph: https://www.desmos.com/calculator/mdgjguyiob

  :param x: the value of the axis
  :param c: the curvature of the axis
  :param b: the deadzone of the axis
  :param dz: the deadzone of the controller
  :return: output speed
  """
  if abs(x) < dz:
    return 0.0
  sign = sgn(x)
  return (abs(x**c) * sign * (1 - b) + b * sign) * scale_speed
