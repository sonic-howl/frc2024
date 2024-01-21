import wpilib
import driveteam
import dashboard
import subsystems

from cscore import CameraServer
from cscore import VideoMode

class MyRobot(wpilib.TimedRobot):

    testmotors = subsystems.ControllerTest()

    def robotInit(self):
        usbCam = CameraServer.startAutomaticCapture()
        mode   = usbCam.getVideoMode()
        print( f"format: {mode.pixelFormat}, fps: {mode.fps}, {mode.width}x{mode.height}")
        #usbCam.setResolution( 640, 480 )
        # kGray appears unsupported
        usbCam.setVideoMode( VideoMode.PixelFormat.kMJPEG, 640, 480, 30 )
        mode   = usbCam.getVideoMode()
        print( f"format: {mode.pixelFormat}, fps: {mode.fps}, {mode.width}x{mode.height}")

    #def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""

    #def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""

    #def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""

    def teleopPeriodic(self):
        # Collect inputs
        cmdX = driveteam.strafeCommand()
        cmdY = driveteam.speedCommand()
        cmdZ = driveteam.rotationCommand()

        intake  = driveteam.pickupCommand()
        trigger = driveteam.shootCommand()

        # Issue Commands
        self.testmotors.move( cmdX, cmdY, cmdZ )
        #self.testmotors.pickup( intake )
        #self.testmotors.shoot( trigger )

        # Update dahboard
        dashboard.lightLed( 0, intake )
        dashboard.lightLed( 1, trigger )

    def teleopExit(self):
        # Stop the shooter
        self.shooter.launch(False)
        self.swervedrive.stop()

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def testExit(self):
        pass

  # def simulationInit(self):
  #   """This function is called once each time the robot enters simulation mode."""

  # def simulationPeriodic(self):
  #   """This function is called periodically during simulation mode."""


if __name__ == "__main__":
  wpilib.run(MyRobot)