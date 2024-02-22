import math

import numpy as np

import constants.RobotConstants as RobotConstants

# Approximate measured Focal Lengths (FL is Focal length), 640 x 480p
MSLifeFL = 625
LogitechFL = 800
TargetSize = 13  # Inches

# Vertical FOV
MSLifeVFOV = math.atan(480 / (2 * MSLifeFL))
LogitechVFOV = math.atan(480 / (2 * LogitechFL))


class kRearCamera:
  x = -RobotConstants.RobotConstants.frame_length / 2
  y = 0
  z = 12
  Elevation = 0
  Rotation = 0
  FL = MSLifeFL

  MinRange = z / math.tan(MSLifeVFOV - Elevation)


print("MSLifeVFOV: " + str(MSLifeVFOV))
print("LogitechVFOV: " + str(LogitechVFOV))
print("Minrange: " + str(kRearCamera.MinRange))
