import math

from wpimath.geometry import Pose2d

MetersPerInch = 0.0254

ShootingRange = 72 * MetersPerInch

## Locations -- https://firstfrc.blob.core.windows.net/frc2024/FieldAssets/2024LayoutMarkingDiagram.pdf, page 4

# Speaker locations
kBlueSpeakerLocation = Pose2d(0, 218.42 * MetersPerInch, math.pi)
kRedSpeakerLocation = Pose2d(652.77 * MetersPerInch, 216.32 * MetersPerInch, 0)
# Amp locations
kBlueAmpLocation = Pose2d(72.5 * MetersPerInch, 323 * MetersPerInch, math.pi / 2)
kRedAmpLocation = Pose2d(578.757 * MetersPerInch, 323 * MetersPerInch, math.pi / 2)
# Pickup locations (Scoring table perspective)
kBluePickupLeftLocation = Pose2d(
  14.02 * MetersPerInch, 34.79 * MetersPerInch, math.pi / 3
)
kBluePickupRightLocation = Pose2d(
  57.54 * MetersPerInch, 9.68 * MetersPerInch, math.pi / 3
)
kRedPickupLeftLocation = Pose2d(
  593.68 * MetersPerInch, 9.68 * MetersPerInch, math.pi * 2 / 3
)
kRedPickupRightLocation = Pose2d(
  637.21 * MetersPerInch, 34.79 * MetersPerInch, math.pi * 2 / 3
)
