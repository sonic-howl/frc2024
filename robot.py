import ntcore
import wpilib
import wpilib.deployinfo
from wpilib.shuffleboard import BuiltInLayouts, Shuffleboard


class MyRobot(wpilib.TimedRobot):
  def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """
    if wpilib.RobotBase.isReal():  # getDeployData() returns None in simulation
      deployArtifacts = wpilib.deployinfo.getDeployData()
      (
        buildArtifacts_layout := Shuffleboard.getTab("metadata")
        .getLayout("DeployArtifacts", BuiltInLayouts.kList)
        .withSize(3, 2)
        .withProperties({"Label position": ntcore._ntcore.Value.makeString("LEFT")})
      )

      buildArtifacts_layout.add("GIT_BRANCH", deployArtifacts["git-branch"])
      buildArtifacts_layout.add("BUILD_DATE", "test")
      buildArtifacts_layout.add("Uncommited Changes", "test")

  def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""

  def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""

  def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""

  def teleopPeriodic(self):
    """This function is called periodically during teleoperated mode."""

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
