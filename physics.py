import pyfrc

class PhysicsEngine( pyfrc.physics.core.PhysicsEngine ):
  
  def __init__(self, physics_controller: pyfrc.physics.core.PhysicsInterface, robot: "MyRobot"):
    pass
  
  def update_sim( self, now: float, tm_diff: float ):
    pass