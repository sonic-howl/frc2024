from typing import TYPE_CHECKING

from pyfrc.physics.core import PhysicsEngine as Engine
from pyfrc.physics.core import PhysicsInterface
from wpilib import DriverStation

if TYPE_CHECKING:
  from robot import Robot


class PhysicsEngine(Engine):
  def __init__(self, physics_controller: PhysicsInterface, robot: "Robot"):
    """Initialize the physics engine with the simulation interface"""

    self.robot = robot
    self.physics_controller = physics_controller

    self.initial_pose_set = False

  def update_sim(self, now: float, tm_diff: float):
    """Called when the simulation parameters for the program need to be updated"""

    assert self.physics_controller.field is not None

    if DriverStation.isAutonomous():
      if not self.initial_pose_set:
        start_pose = self.robot.startingPose

        if start_pose is not None:
          self.physics_controller.field.setRobotPose(start_pose)
          self.robot.drivebase.resetOdometer(start_pose)

        self.initial_pose_set = True
    elif DriverStation.isTest():
      self.initial_pose_set = False

    if DriverStation.isDisabled():
      self.initial_pose_set = False
    else:
      chassis_speeds = self.robot.drivebase.simChassisSpeeds
      if chassis_speeds is not None:
        pose = self.physics_controller.drive(chassis_speeds, tm_diff)

        self.physics_controller.field.setRobotPose(pose)
        self.robot.drivebase.resetOdometer(pose)
