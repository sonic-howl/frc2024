import rev
import wpilib

motor1 = rev.CANSparkMax(1, rev.CANSparkLowLevel.MotorType.kBrushless)
motor2 = rev.CANSparkMax(2, rev.CANSparkLowLevel.MotorType.kBrushless)


def stop():
  motor1.set(0.0)
  motor2.set(0.0)


def shoot(fire: float):
  if fire <= 0.05:
    stop()
  else:
    motor1.set(-fire)
    motor2.set(fire)


def elevate(elevate: float):
  pass
  # TBD
