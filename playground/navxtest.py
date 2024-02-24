import math

import navx
import wpilib
import wpilib.simulation

class GyroBot(wpilib.TimedRobot):
  """
  Class to experiment with gyro library in simulation
  """
  def robotInit(self):
    self.gyro = navx.AHRS( wpilib.SerialPort.Port.kMXP, navx.AHRS.SerialDataType.kProcessedData, 50 )
    self.angle = 0.0
    self.yaw   = 0.0
    self.last_angle = self.angle
    self.last_yaw   = self.yaw
    print( self.angle )
    print( self.yaw )
    print( wpilib.simulation.SimDeviceSim.enumerateDevices() )
    self.sim_gyro = wpilib.simulation.SimDeviceSim( "navX-Sensor[1]" )
    print( self.sim_gyro.enumerateValues() )

  def readGyro(self):
    # Will alter angles through simulator
    self.angle = self.gyro.getAngle()
    self.yaw   = self.gyro.getYaw()
    if self.angle != self.last_angle or self.yaw != self.last_yaw:
      print( self.angle )
      print( self.yaw )
    self.last_angle = self.angle
    self.last_yaw   = self.yaw

  def autonomousInit(self) -> None:
    self.gyro.setAngleAdjustment( 90 )
    
  def autonomousPeriodic(self):
    self.readGyro()

  def teleopPeriodic(self):
    self.readGyro()


if __name__ == "__main__":
  wpilib.run(GyroBot)
