import wpilib

class DriveTeam:

    pilot = wpilib.XboxController(0)

    #copilot = 

    def get_strafe_commands(self): 
        return self.pilot.getLeftX() 

    def get_drive_commands(self): #translational(foward/backward)
        return self.pilot.getLeftY()

    def get_turn(self): #left/right
        return self.pilot.getRightX()
    
    def get_shoot_commands(self):
        return self.pilot.getRightBumper()
    
    

