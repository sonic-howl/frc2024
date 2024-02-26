# Module for drive team commands
# Includes real controller commands and simulated controls
import ntcore
import wpilib

from constants.ntconstants import SimTable

class DriveTeam:
  def __init__(self):
    # Treat controller instances as private, use the functions below to access controls.
    self.pilot   = wpilib.PS4Controller(0)
    self.copilot = wpilib.PS4Controller(1)

    # Set up network tables
    network_table = ntcore.NetworkTableInstance.getDefault()
    sim_table = network_table.getTable( SimTable.name )
    self.x_pub = sim_table.getFloatTopic( SimTable.x ).publish()
    self.y_pub = sim_table.getFloatTopic( SimTable.y ).publish()
    self.r_pub = sim_table.getFloatTopic( SimTable.r ).publish()
    self.x_pub.set(0.0)
    self.y_pub.set(0.0)
    self.r_pub.set(0.0)
    # Listen for control changes at the drive station boards
    self.x_sub = sim_table.getFloatTopic( SimTable.x ).subscribe(0.0)
    self.y_sub = sim_table.getFloatTopic( SimTable.y ).subscribe(0.0)
    self.r_sub = sim_table.getFloatTopic( SimTable.r ).subscribe(0.0)


  def strafe_command(self) -> float:
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
    if wpilib.RobotBase.isReal():
      return -self.pilot.getLeftX()
    else:
      return -self.x_sub.get()

  def drive_command(self) -> float:
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
    if wpilib.RobotBase.isReal():
      return -self.pilot.getLeftY()
    else:
      return -self.y_sub.get()

  def turn_command(self) -> float:
    """
    Returns the rotation command (z) to the robot
    In all views, rotation direction viewed from overhead:
      -z rotate counterclockwise (+z) in robot coordinates
      +z rotate counterclockwise (-z) in robot coordinates
    """
    if wpilib.RobotBase.isReal():
      return -self.pilot.getRightX()
    else:
      return -self.r_sub.get()

  def get_winch_command(self) -> bool:  # deploy winch
    return False #pilot.getStartButton() # Need a PS4 alternative

  def get_hook_extension_command(self):
    return self.pilot.getPOV() == 0

  def get_hook_retract_command(self):
    return self.pilot.getPOV() == 270

  def get_hook_left_command(self):
    return self.pilot.getPOV() == 90

  def get_hook_right_command(self):
    return self.pilot.getPOV() == 180

  def get_aim_command(self):  # raise/lower shooter
    return self.copilot.getLeftY()

  def launch_command(self) -> bool:  # shoot shooter
    return self.copilot.getR1Button()

  def unjam_command(self) -> bool:  # unjam shooter
    return self.copilot.getR2Button()

  def pickup_command(self) -> bool:  # used to pickup rings
    return self.copilot.getL1Button()

  def eject_command(self) -> bool:  # eject stuck note from bottom
    return self.copilot.getL2Button()

  def get_test_command(self):
    return self.pilot.getAButton()

  def get_test_command2(self):
    return self.copilot.getAButton()
