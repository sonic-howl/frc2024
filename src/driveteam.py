import wpilib


class DriveTeam:
  def __init__(self):
    self.pilot = wpilib.XboxController(0)
    self.copilot = wpilib.XboxController(1)

  ### Pilot ###
  def get_strafe_command(self):
    return -self.pilot.getLeftX()

  def get_drive_command(self):  # translational(foward/backward)
    return -self.pilot.getLeftY()

  def get_turn_command(self):  # left/right
    return -self.pilot.getRightX()

  def get_winch_command(self):  # deploy winch
    return self.pilot.getStartButton()

  def get_hook_extension_command(self):
    return self.pilot.getPOV() == 0

  def get_hook_retract_command(self):
    return self.pilot.getPOV() == 270

  def get_hook_left_command(self):
    return self.pilot.getPOV() == 90

  def get_hook_right_command(self):
    return self.pilot.getPOV() == 180

  def get_view_command(self) -> bool:  # swap between 3rd & first person view
    return self.pilot.getBackButtonPressed()

  def get_move_to_amp_command(self):
    return self.pilot.getYButton()

  def get_move_to_speaker_command(self):
    return self.pilot.getAButton()

  def get_move_to_pickup_left_command(self):
    return self.pilot.getXButton()

  def get_move_to_pickup_right_command(self):
    return self.pilot.getBButton()

  ### Copilot ###
  def get_aim_command(self) -> float:  # raise/lower shooter
    return self.copilot.getLeftY()

  def get_firing_command(self) -> float:  # shoot shooter
    return self.copilot.getLeftTriggerAxis()

  def get_unjam_command(self) -> bool:  # unjam shooter
    return self.copilot.getLeftBumper()

  def get_pickup_command(self) -> float:  # used to pickup rings
    return self.copilot.getRightTriggerAxis()

  def get_eject_command(self) -> bool:  # eject stuck note
    return self.copilot.getRightBumper()

  def get_test_command2(self):
    return self.copilot.getAButton()
