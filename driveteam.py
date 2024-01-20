import wpilib


class DriveTeam:
  pilot = wpilib.XboxController(0)

  copilot = wpilib.XboxController(1)

  def get_strafe_commands(self):
    return self.pilot.getLeftX()

  def get_drive_commands(self):  # translational(foward/backward)
    return self.pilot.getLeftY()

  def get_turn_commands(self):  # left/right
    return self.pilot.getRightX()

  def get_winch_commands(self):  # deploy winch
    return self.pilot.getStartButton()

  def get_hook_extension_commands(self):
    return self.pilot.getPOV() == 0

  def get_hook_retract_commands(self):
    return self.pilot.getPOV() == 270

  def get_hook_left_commands(self):
    return self.pilot.getPOV() == 90

  def get_hook_right_commands(self):
    return self.pilot.getPOV() == 180

  def get_aim_commands(self):  # raise/lower shooter
    return self.copilot.getLeftY()

  def get_firing_commands(self):  # shoot shooter
    return self.copilot.getLeftTriggerAxis()

  def get_unjam_commands(self):  # unjam shooter
    return self.copilot.getLeftBumper()

  def get_pickup_commands(self):  # used to pickup rings
    return self.copilot.getRightTriggerAxis()

  def get_eject_commands(self):  # eject stuck note
    return self.copilot.getRightBumper()

  def get_test_commands(self):
    return self.pilot.getAButton()

  def get_test_commands2(self):
    return self.copilot.getAButton()
