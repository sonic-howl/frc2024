import rev
import wpilib


class Launchers:
  def __init__(self):
    self.motor1 = rev.CANSparkMax(10, rev.CANSparkLowLevel.MotorType.kBrushless)

    self.motor2 = rev.CANSparkMax(11, rev.CANSparkLowLevel.MotorType.kBrushless)

    self.feed = rev.CANSparkMax(12, rev.CANSparkLowLevel.MotorType.kBrushless)

    if wpilib.RobotBase.isReal():
      self.elevator = rev.CANSparkMax(13, rev.CANSparkLowLevel.MotorType.kBrushed)
    else:
      self.elevator = rev.CANSparkMax(13, rev.CANSparkLowLevel.MotorType.kBrushless)

    # Limit switches
    self.upperswitch = wpilib.DigitalInput(1)
    self.lowerswitch = wpilib.DigitalInput(2)
    self.feedswitch = wpilib.DigitalInput(0)

    self.feed_amp_counter = 0
    self.firetimer = 75

  def stop(self):
    self.motor1.set(0.0)
    self.motor2.set(0.0)
    self.feed.set(0.0)
    self.elevator.set(0.0)
    self.firetimer = 75  # In robot cycles

  def shoot(self, fire: float):
    if fire <= 0.05:
      self.stop()
    else:
      # Stop unrelated motors
      # self.elevator.set(0.0)
      # Spool up rollers
      self.motor1.set(-fire)
      self.motor2.set(fire)
      self.firetimer = self.firetimer - 1

      # Feed ring into launcher when we are at the lowered position
      if self.firetimer <= 0:  # and check launcher is lowered
        self.feed.set(1.0)
      else:
        self.feed.set(0.0)
      # If we weren't lowered we have probably already dropped the note into the amp.

  def unjams(self):
    # Stop unrelated motors
    # self.elevator.set(0.0)
    # Reverse rollers
    self.motor1.set(0.25)
    self.motor2.set(-0.25)
    self.feed.set(-0.5)

  ### Elevator is currently not physically implemented. Might be added later. ###
  # def elevate(self, elevate: float):
  #   # Stop unrelated motors
  #   self.motor1.set(0.0)
  #   self.motor2.set(0.0)

  #   isGoingDown = elevate <= 0
  #   is_upper_switch_on = self.upperswitch.get()
  #   is_lower_switch_on = self.lowerswitch.get()

  #   if abs(elevate) <= 0.05:
  #     self.feed.set(0.0)
  #     self.elevator.set(0.0)
  #     if is_lower_switch_on:
  #       # Set up timer to push note into launcher
  #       self.feed_amp_counter = 25  # Adjust on testing, 25x20ms cycles is a half second
  #   elif isGoingDown:
  #     # Feed is not used in descent
  #     self.feed.set(0.0)
  #     if is_lower_switch_on:
  #       # Do not descend when lower switch is reached
  #       self.elevator.set(0.0)
  #     else:
  #       self.elevator.set(elevate)
  #   else:  # not isGoingDown, i.e. going up
  #     if is_lower_switch_on:
  #       if self.feed_amp_counter > 0:
  #         # Push note into launcher
  #         self.elevator.set(0.0)
  #         self.feed.set(0.2)
  #         self.feed_amp_counter -= 1
  #       else:
  #         # We are ready to raise
  #         self.elevator.set(elevate)
  #         self.feed.set(0.0)
  #     elif is_upper_switch_on:
  #       # Do not raise when upper switch is reached
  #       self.elevator.set(0.0)
  #       self.feed.set(0.0)
  #     else:
  #       self.elevator.set(elevate)
  #       self.feed.set(0.0)

  def pickup(self):
    # Stop unrelated motors
    self.motor1.set(0.0)
    self.motor2.set(0.0)
    # self.elevator.set(0.0)
    # Stop when note reaches limit switch in the feed mechanism
    if not self.feedswitch.get():
      self.feed.set(0.0)
    else:
      # Choose speed to ensure we don't overshoot limit switch
      self.feed.set(0.5)

  def eject(self):
    # Stop unrelated motors
    self.motor1.set(0.0)
    self.motor2.set(0.0)
    # self.elevator.set(0.0)
    # Push note back out the pickup
    self.feed.set(-1.0)
