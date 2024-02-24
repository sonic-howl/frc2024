import pyfrc

class PhysicsEngine( pyfrc.physics.core.PhysicsEngine ):
  
  def __init__(self, physics_controller: pyfrc.physics.core.PhysicsInterface, robot: "MyRobot"):
    pass
    # self.drive_fl = robot.drivebase.front_left.drive_motor.getSimCollection()
    # self.drive_fr = robot.drivebase.front_right.drive_motor.getSimCollection()
    # self.drive_bl = robot.drivebase.back_left.drive_motor.getSimCollection()
    # self.drive_br = robot.drivebase.back_right.drive_motor.getSimCollection()
  
  def update_sim( self, now: float, tm_diff: float ):
    pass