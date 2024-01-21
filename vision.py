import cscore

def run():
    usbCam = cscore.CameraServer.startAutomaticCapture()
    usbCam.setResolution( 640, 480 )
    while True:
        pass

if __name__ == "__main__":
    run()
