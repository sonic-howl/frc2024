import wpilib
import rev
import phoenix6

# Dummy 'drive base' for experimenting with motor controllers in simulation
class ControllerTest:

    # Dummy motor types for testing simulator
    mot0 = wpilib.PWMSparkMax(2)
    mot1 = wpilib.PWMVictorSPX(3)
    mot2 = wpilib.PWMVenom(4)
    mot3 = rev.CANSparkMax(5,rev.CANSparkLowLevel.MotorType.kBrushless)
    mot4 = phoenix6.hardware.TalonFX(6)

    cmdMot4 = phoenix6.controls.DutyCycleOut(0.)

    # Movement left/right, forward/back, rotate left/right
    def move( self, x, y, z ):
        self.mot0.set(x)
        self.mot1.set(y)
        self.mot2.set(z)
        self.mot3.set(x)
        #self.mot4.set( phoenix6.ControlMode.Velocity, y )
        self.mot4.set_control( self.cmdMot4.with_output(y) )
        

    def stop(self):
        self.mot0.set(0.)
        self.mot1.set(0.)
        self.mot2.set(0.)
        self.mot3.set(0.)
        #self.mot4.set( phoenix6.ControlMode.Velocity, 0. )
        self.mot4.set_control( self.cmdMot4.with_output(0.) )

