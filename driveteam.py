import wpilib

# Treat controller instances as private, use the functions below to access controls.
pilot   = wpilib.PS4Controller(0)
copilot = wpilib.PS4Controller(1)

def get_strafe_command():
  return pilot.getLeftX()

def get_drive_command():  # translational(foward/backward)
  return pilot.getLeftY()

def get_turn_command():  # left/right
  return pilot.getRightX()

def get_winch_command():  # deploy winch
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

def launch_command():  # shoot shooter
  return copilot.getR1Button()

def unjam_command():  # unjam shooter
  return copilot.getL2Button() #XBOX copilot.getLeftBumper()

def pickup_command():  # used to pickup rings
  return copilot.getL1Button()

def eject_command():  # eject stuck note
  return copilot.getR2Button() #XBOX copilot.getRightBumper()

def get_test_command():
  return pilot.getAButton()

def get_test_command2():
  return copilot.getAButton()
