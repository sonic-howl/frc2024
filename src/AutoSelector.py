import json
import os
import typing

import wpilib as wp
from pathplannerlib.auto import AutoBuilder, PathPlannerAuto
from wpimath.geometry import Pose2d


def findAutos() -> typing.Dict[str, typing.Tuple[Pose2d, PathPlannerAuto]]:
  autosPath = os.path.join(wp.getDeployDirectory(), "pathplanner", "autos")

  autos = {}
  for file in os.listdir(autosPath):
    if file.endswith(".auto"):
      with open(os.path.join(autosPath, file), "r") as f:
        auto_json = json.loads(f.read())
        starting_pose = None
        try:
          starting_pose = AutoBuilder.getStartingPoseFromJson(auto_json["startingPose"])
        except KeyError:
          pass
        autos[file.split(".auto")[0]] = (
          starting_pose,
          AutoBuilder.getAutoCommandFromJson(auto_json),
        )

  return autos


class AutoSelector:
  def __init__(self):
    self.autoSelector = wp.SendableChooser()
    autos = findAutos()

    # TODO make a better way to find the default auto
    # by getting the pose of the robot from the camera as it's disabled, use the auto with the closest starting pose
    defaultAuto = None
    closestDistance = float("inf")
    for autoName, auto in autos.items():
      pose = auto[0]
      if pose is None:
        continue
      if defaultAuto is None:
        defaultAuto = auto
        continue
      distance = pose.translation().distance(defaultAuto[0].translation())
      if distance < closestDistance:
        closestDistance = distance
        defaultAuto = auto

    self.autoSelector.setDefaultOption(autoName, auto)

    for autoName, auto in autos.items():
      if auto is defaultAuto:
        continue
      self.autoSelector.addOption(autoName, auto)

    wp.SmartDashboard.putData("Auto Selector", self.autoSelector)

    self.lastAutoSelected = None

  def getSelectedAuto(self) -> typing.Tuple[Pose2d | None, PathPlannerAuto]:
    return self.autoSelector.getSelected()
