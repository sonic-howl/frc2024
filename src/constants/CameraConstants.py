import math

from constants.RobotConstants import RobotConstants

# Approximate measured Focal Lengths (FL is Focal length), at 640 x 480p
MSLifeFL = 625
LogitechFL = 800
TargetSize = 13  # Inches

# Vertical FOV
MSLifeVFOV = math.atan(480 / (2 * MSLifeFL))
LogitechVFOV = math.atan(480 / (2 * LogitechFL))


class kRearCamera:
  # In radians
  Elevation = math.radians(-10)
  Rotation = 0  # Always at 0
  FOV = MSLifeVFOV

  # In inches, robot coordinates
  x = -RobotConstants.frame_length / 2
  y = 0
  z = 12
  MinRange = z / math.tan(FOV - Elevation)

  # In pixels
  FL = MSLifeFL
  HorizonShift = int(FL * ((math.tan(Elevation)) / (math.cos(Elevation))))
