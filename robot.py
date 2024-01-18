import wpilib
import driveteam






class MyRobot(wpilib.TimedRobot):
  
  pilots = driveteam.DriveTeam() 
  strafe = 0.
  turn = 0.
  drive = 0.

  def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """

  def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""

  def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""

  def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""

  def teleopPeriodic(self):
    """This function is called periodically during teleoperated mode."""
    self.strafe = self.pilots.get_strafe_commands()
    self.turn = self.pilots.get_turn()
    self.drive = self.pilots.get_drive_commands()
    if self.pilots.get_shoot_commands():
      print(f"{self.strafe}, {self.turn}, {self.drive}")
    


  def testInit(self):
    """This function is called once each time the robot enters test mode."""

  def testPeriodic(self):
    """This function is called periodically during test mode."""

  # def simulationInit(self):
  #   """This function is called once each time the robot enters simulation mode."""

  # def simulationPeriodic(self):
  #   """This function is called periodically during simulation mode."""


if __name__ == "__main__":
  wpilib.run(MyRobot)

