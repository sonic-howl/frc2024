import wpilib

# Treat controller instances as private, use the functions below to access controls.
pilot   = wpilib.PS4Controller(0)
copilot = wpilib.PS4Controller(1)

def strafe_command() -> float:
  """
  Returns the lateral translation command (x) to the robot
  FPV (first person view):
    -x strafe left (+y) in robot coordinates
    +x strafe right (-y) in robot coordinates
  TPV (third person view from the alliance area)
    -x strafe left (+y) in field coordinates
    +x strafe right (-y) in field coordinates
    Third person commands need to be reversed for red alliance on a mirrored field layout.
  """
  return -pilot.getLeftX()

def drive_command() -> float:
  """
  Returns the longitudinal translation command (y) to the robot
  FPV (first person view):
    -y advance (+x) in robot coordinates
    +y reverse (-x) in robot coordinates
  TPV (third person view from the alliance area)
    -y advance (+y) in field coordinates
    +y reverse (-y) in field coordinates
    Third person commands need to be reversed for red alliance on a mirrored field layout.
  Note above assumes typical inverted y axis on the joystick (like an airplane).
  If the input is not inverted, remove the negative sign on the return value.
  """
  return -pilot.getLeftY()

def turn_command() -> float:
  """
  Returns the rotation command (z) to the robot
  In all views, rotation direction viewed from overhead:
    -z rotate counterclockwise (+z) in robot coordinates
    +z rotate counterclockwise (-z) in robot coordinates
  """
  return -pilot.getRightX()

def get_winch_command() -> bool:  # deploy winch
  return False #pilot.getStartButton() # Need a PS4 alternative

def get_hook_extension_command():
  return pilot.getPOV() == 0

def get_hook_retract_command():
  return pilot.getPOV() == 270

def get_hook_left_command():
  return pilot.getPOV() == 90

def get_hook_right_command():
  return pilot.getPOV() == 180

def get_aim_command():  # raise/lower shooter
  return copilot.getLeftY()

def launch_command() -> bool:  # shoot shooter
  return copilot.getR1Button()

def unjam_command() -> bool:  # unjam shooter
  return copilot.getR2Button()

def pickup_command() -> bool:  # used to pickup rings
  return copilot.getL1Button()

def eject_command() -> bool:  # eject stuck note from bottom
  return copilot.getL2Button()

def get_test_command():
  return pilot.getAButton()

def get_test_command2():
  return copilot.getAButton()
