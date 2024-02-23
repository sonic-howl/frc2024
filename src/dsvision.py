import cv2

from constants.CameraConstants import kRearCamera


def Initialization():
  TargetSize = 13  # Note (foam ring) diameter in inches

  global guidelineSpacing
  guidelineSpacing = int(kRearCamera.FL * TargetSize / kRearCamera.MinRange)
  global guidelineXOffset
  guidelineXOffset = int(kRearCamera.FL * (kRearCamera.y / kRearCamera.MinRange))


def get_capture(window_name, video_capture_device_index=0):
  # localsim = "http://localhost:1181/?action=stream"
  roborio = "http://roboRIO-3985-frc.local:1181/?action=stream"  # IP depends on connection method (USB Tether, Ethernet, Radio)
  # Create a window named 'window_name'
  cv2.namedWindow(window_name)
  # Open the Webcam
  # For a usb camera provide port number
  # For a stream provide the URL of the video feed
  # cap = cv2.VideoCapture(video_capture_device_index)
  cap = cv2.VideoCapture(roborio)
  return cap


def draw_overlay():
  # Get the height and width of the frame
  height, width, channels = frame.shape
  VanishingPointX = width // 2
  VanishingPointY = height // 2 + kRearCamera.HorizonShift
  # Draw a circle in the center of the frame
  cv2.circle(frame, (width // 2, height // 2), 50, (0, 0, 255), 1)
  # Draw lines representing the width of the note at specific distances
  cv2.line(
    frame,
    (VanishingPointX, VanishingPointY),
    (width // 2 - guidelineSpacing // 2 - guidelineXOffset, height),
    (0, 255, 0),
    1,
  )
  cv2.line(
    frame,
    (VanishingPointX, VanishingPointY),
    (width // 2 + guidelineSpacing // 2 - guidelineXOffset, height),
    (0, 255, 0),
    1,
  )
  # Draw the horizon
  cv2.line(frame, (0, VanishingPointY), (width, VanishingPointY), (0, 255, 0), 1)
  # Draw a text on the frame
  cv2.putText(
    frame,
    "q to quit",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 255, 255),
    1,
  )


def show_capture(capture_window_name, capture):
  while True:
    # Capture frame-by-frame
    global frame
    ret, frame = capture.read()
    if frame is not None:
      draw_overlay()
      # Display the resulting frame in the named window
      cv2.imshow(capture_window_name, frame)
    else:
      break
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break


def cleanup_capture(capture):
  # When everything done, release the capture
  capture.release()
  cv2.destroyAllWindows()


def main():
  Initialization()
  capture_window_name = "Pickup Camera"
  capture = get_capture(capture_window_name, 0)

  # Loop while processing images.
  show_capture(capture_window_name, capture)

  cleanup_capture(capture)


if __name__ == "__main__":
  main()
