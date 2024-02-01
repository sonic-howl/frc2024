import wpilib
#import rev
#import phoenix6

# Dummy subsystems for experimenting with motor controllers in simulation
class ControllerTest:

    def __init__(self) -> None:
        # Dummy motor types for testing simulator
        self.mot0 = wpilib.PWMSparkMax(0)
        self.mot1 = wpilib.PWMVictorSPX(1)
        self.mot2 = wpilib.PWMTalonSRX(2)
        #self.mot3 = rev.CANSparkMax(3,rev.CANSparkLowLevel.MotorType.kBrushless)
        #self.mot4 = phoenix6.hardware.TalonFX(4)
        #self.cmdMot4 = phoenix6.controls.DutyCycleOut(0.)

    # Movement left/right, forward/back, rotate left/right
    def move( self, x: float, y:float, z: float ):
        self.mot0.set(x)
        self.mot1.set(y)
        self.mot2.set(z)

    def pickup( self, on: bool ):
        pass
        """
        if on:
            self.mot3.set(1.)
        else:
            self.mot3.set(0.)
        """

    def shoot( self, on: bool ):
        pass
        """
        if on:
            self.mot4.set_control( self.cmdMot4.with_output(1.) )
        else:
            self.mot4.set_control( self.cmdMot4.with_output(0.) )
        """

    def stop(self):
        self.mot0.set(0.)
        self.mot1.set(0.)
        self.mot2.set(0.)
        #self.mot3.set(0.)
        #self.mot4.set( phoenix6.ControlMode.Velocity, 0. )
        #self.mot4.set_control( self.cmdMot4.with_output(0.) )

