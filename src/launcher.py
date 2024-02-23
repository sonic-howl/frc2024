import rev
import wpilib


class Launchers:
  def __init__(self):
    self.motor1 = rev.CANSparkMax(10, rev.CANSparkLowLevel.MotorType.kBrushless)

    self.motor2 = rev.CANSparkMax(11, rev.CANSparkLowLevel.MotorType.kBrushless)

    self.elevator = rev.CANSparkMax(12, rev.CANSparkLowLevel.MotorType.kBrushed)

    self.encoder1 = self.motor1.getEncoder()

    self.encoder2 = self.motor2.getEncoder()

    self.upperswitch = wpilib.DigitalInput(0)

    self.lowerswitch = wpilib.DigitalInput(1)

  def stop(self):
    self.motor1.set(0.0)
    self.motor2.set(0.0)
    self.elevator.set(0.0)

  def shoot(self, fire: float):
    if fire <= 0.05:
      self.stop()
    else:
      self.motor1.set(-fire)
      self.motor2.set(fire)

      #  self.launcher_RPM1 = RPMInfo_layout.add( "Launcher_RPM1", launcher.encoder1.getVelocity()).getEntry()
      #  self.launcher_RPM2 = RPMInfo_layout.add("Launcher_RPM2", launcher.encoder2.getVelocity()).getEntry()

      if self.encoder1.getVelocity() < -4500.0 and self.encoder2.getVelocity() > 4500.0:
        pass
      # feed ring into launcher

  def unjams(self):
    self.motor1.set(0.5)
    self.motor2.set(-0.5)

  def elevate(self, elevate: float):
    isGoingDown = elevate <= 0
    is_upper_switch_on = self.upperswitch.get()
    is_lower_switch_on = self.lowerswitch.get()

    if abs(elevate) <= 0.05():
      self.stop()
    elif isGoingDown and is_lower_switch_on:
      self.stop()
    elif not isGoingDown and is_upper_switch_on:
      self.stop()
    else:
      self.elevator.set(elevate)
