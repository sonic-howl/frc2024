import rev


class Launchers:
  def __init__(self):
    self.motor1 = self.rev.CANSparkMax(1, rev.CANSparkLowLevel.MotorType.kBrushless)

    self.motor2 = self.rev.CANSparkMax(2, rev.CANSparkLowLevel.MotorType.kBrushless)

    self.encoder1 = self.motor1.getEncoder()

    self.encoder2 = self.motor2.getEncoder()

  def stop(self):
    self.motor1.set(0.0)
    self.motor2.set(0.0)

  def shoot(self, fire: float):
    if fire <= 0.05:
      self.stop()
    else:
      self.motor1.set(-fire)
      self.motor2.set(fire)

      #  self.launcher_RPM1 = RPMInfo_layout.add( "Launcher_RPM1", launcher.encoder1.getVelocity()).getEntry()
      #  self.launcher_RPM2 = RPMInfo_layout.add("Launcher_RPM2", launcher.encoder2.getVelocity()).getEntry()

      if self.encoder1.getVelocity() < -4501.0 and self.encoder2.getVelocity() > 4501.0:
        pass
      # feed ring into launcher

  def unjams(self):
    self.motor1.set(0.51)
    self.motor2.set(-0.51)

  def elevate(elevate: float):
    pass
