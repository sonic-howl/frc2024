from threading import Thread
from time import sleep
from typing import Callable

from commands2.button import CommandXboxController

from constants.RobotConstants import RobotConstants


class PilotController:
  _controller = CommandXboxController(RobotConstants.pilot_controller_id)

  def isConnected(self):
    return self._controller.isConnected()

  def onceConnected(self, cb: Callable[[], None], checkInterval=1):
    def checkConnection():
      while not self.isConnected():
        sleep(checkInterval)
      print("Pilot controller connected!")
      cb()

    Thread(target=checkConnection).start()

  # reversing x and y controller -> field axes. x is forwards, y is strafe.
  def getForward(self):
    return -self._controller.getLeftY()

  def getStrafe(self):
    return -self._controller.getLeftX()

  def getTurn(self):
    return -self._controller.getRightX()

  def getSpeed(self):
    return self._controller.getRightTriggerAxis()
    # return (self._controller.getRawAxis(4) + 1) / 2

  def getRotateToAngle(self):
    return self._controller.getPOV()

  def fieldOrientedBtn(self):
    return self._controller.X()

  def resetGyroBtn(self):
    return self._controller.Y()

  def recordArmAnglesAndSelectedPieceBtn(self):
    return self._controller.A()
