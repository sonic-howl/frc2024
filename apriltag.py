# This is a quick demo of the apriltag detection and applying overlays
# to a webcam camera stream. Use as inspiration or reference for robot vision.
# original file: https://gist.github.com/lobrien/5d5e1b38e5fd64062c43ac752b74889c

import cv2
import robotpy_apriltag
import math
import wpimath.geometry

from constants.ntconstants import VisionTable

# Allows us to report back to robot
from ntcore import NetworkTableInstance
network_table_instance = NetworkTableInstance.getDefault()
vision_dashboard = network_table_instance.getTable( VisionTable.name )
bot_pose_pub = vision_dashboard.getFloatArrayTopic( VisionTable.bot_pose ).publish()
tag_pose_pub = vision_dashboard.getFloatArrayTopic( VisionTable.tag_pose ).publish()

field  = robotpy_apriltag.loadAprilTagLayoutField(robotpy_apriltag.AprilTagField.k2024Crescendo)
rot000 = wpimath.geometry.Rotation3d( 0.0, 0.0,      0.0 )   #   0 degree rotation in xy plane
rot090 = wpimath.geometry.Rotation3d( 0.0, 0.0,  math.pi/2 ) #  90 degree rotation in xy plane
rot180 = wpimath.geometry.Rotation3d( 0.0, 0.0, -math.pi  )  # 180 degree rotation in xy plane
rot270 = wpimath.geometry.Rotation3d( 0.0, 0.0, -math.pi/2 ) # -90 degree rotation in xy plane

bot_pose = wpimath.geometry.Pose2d()

# This function is called once to initialize the apriltag detector and the pose estimator
def get_apriltag_detector_and_estimator( width: float, height: float ):
    detector = robotpy_apriltag.AprilTagDetector()
    # FRC 2024 uses tag36h11
    assert detector.addFamily("tag36h11")

    # Focal lengths need to be characterised for robot camera.
    tagSize = 6.5 * 0.0254 # 6.5 inches convert to meters
    # rough focal length measure using ruler as target.
    fx = width  * 14.6875/12.0 # 14"11/16
    fy = height * 20.75/12.0   # 20" 3/4
    estimator = robotpy_apriltag.AprilTagPoseEstimator(
    robotpy_apriltag.AprilTagPoseEstimator.Config(
            tagSize, fx, fy, width / 2.0, height / 2.0
        )
    )
    return detector, estimator
    
# This simply outputs some information about the results returned by `process_apriltag`.
# It prints some info to the console and draws a circle around the detected center of the tag
# Illustrates how you can add target reticles or other drive team aids to the camera view.
def draw_tag( result ):
    assert frame is not None
    assert result is not None
    tag_id, pose, center = result
    if tag_id>0:
      cv2.circle(frame, (int(center.x), int(center.y)), 50, (255, 0, 255), 3)
      msg  = f"Tag ID: {tag_id}"
      msg2 = f"Pose T: {pose.translation().X():.2f}, {pose.translation().Y():.2f}, {pose.translation().Z():.2f}"
      msg3 = f"Pose R: {pose.rotation().X():.3f}, {pose.rotation().Y():.3f}, {pose.rotation().Z():.3f}"
      # Get tag location on the field
      tagPose = field.getTagPose( tag_id )
      tagLoc  = tagPose.translation()
      tagRot  = tagPose.rotation()
      msg4 = f"Tag T: {tagLoc.X():.3f}, {tagLoc.Y():.3f}, {tagLoc.Z():.3f}"
      msg5 = f"Tag R: {tagRot.X():.3f}, {tagRot.Y():.3f}, {tagRot.Z():.3f}"
      msg6 = f"Bot Pose: x{bot_pose.X():.3f} y{bot_pose.Y():.3f} r{bot_pose.rotation().radians():.3f}"
      cv2.putText(frame, msg,  (150, 50 * 1), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 100), 2)
      cv2.putText(frame, msg2, ( 50, 50 * 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 100), 2)
      cv2.putText(frame, msg3, ( 50, 50 * 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 100), 2)
      cv2.putText(frame, msg4, ( 50, 50 * 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 100), 2)
      cv2.putText(frame, msg5, ( 50, 50 * 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 100), 2)
      cv2.putText(frame, msg6, ( 50, 50 * 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 100), 2)

# This function is called for every detected tag. It uses the `estimator` to 
# return information about the tag, including its centerpoint. (The corners are 
# also available.)
def process_apriltag(estimator, tag):
    tag_id = tag.getId()
    center = tag.getCenter()

    est = estimator.estimateOrthogonalIteration(tag, 50)

    # Filter out zero poses that apriltag library can return due to errors
    if est.pose1.translation().Z()>0.01:
      tag_pose = est.pose1
      # Disambiguate pose, choose closest to vertical (TBD adjust for camera elevation).
      if est.pose2.translation().Z()>0.01 and abs(est.pose2.rotation().X())<abs(est.pose1.rotation().X()):
        tag_pose = est.pose2
    else:
      # Discarded both poses
      tag_id = 0  

    return tag_id, tag_pose, center

# This function is called once for every frame captured by the Webcam. For testing, it can simply
# be passed a frame capture loaded from a file. (See commented-out alternative `if __name__ == main:` at bottom of file)
def detect_and_process_apriltag( detector, estimator ):
    assert frame is not None
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect apriltag
    tag_info = detector.detect(gray)
    DETECTION_MARGIN_THRESHOLD = 100
    filter_tags = [tag for tag in tag_info if tag.getDecisionMargin() > DETECTION_MARGIN_THRESHOLD]
    #results = [ process_apriltag(estimator, tag) for tag in filter_tags ]
    best_tag_id = 0
    for tag in filter_tags:
      result = process_apriltag( estimator, tag )
      if result[0]>0: # Screen for tags that had no useful poses
        if best_tag_id==0 or result[1].translation().norm()<best_result[1].translation().norm(): # Pick closest tag if there are multiple choices
          best_tag_id = result[0]
          best_result = result

    if best_tag_id>0:
      # Compute robot pose for the preferred tag

      # Get pose in field coordinates
      field_pose = field.getTagPose( best_tag_id )
      # Apriltag defines orientation into tag, field out of so rotating 180 degrees
      correction = wpimath.geometry.Transform3d( wpimath.geometry.Translation3d( 0.0, 0.0, 0.0), rot180 ) 
      field_pose = field_pose.transformBy( correction )

      # Get camera position
      # 1) Convert pose estimate transform from camera coordinates frame to robot coordinate frame
      # 2) Create pose at origin for camera position, transform to get tag position
      # 3) Reset the origin at the tag
      # 4) Apply a rigid body transform (using the defined tag pose on the field) to compute robot pose on the field 
      tag_pose = best_result[1]
      T1 = wpimath.geometry.CoordinateSystem.convert( tag_pose, wpimath.geometry.CoordinateSystem.EDN(), wpimath.geometry.CoordinateSystem.NWU() )
      bc = wpimath.geometry.Pose3d()
      bt = bc.transformBy(T1)
      # TBD can correct for camera position and orientation here and generate bb, the bot frame center
      bc = bc.relativeTo(bt)
      bt = bt.relativeTo(bt)
      fc = bc.rotateBy( field_pose.rotation() )
      fc = wpimath.geometry.Pose3d( fc.translation()+field_pose.translation(), fc.rotation() )
      # Publish bot pose (should be done on detection for time stamping)
      global bot_pose
      bot_pose = fc.toPose2d()
      bot_pose_pub.set( [bot_pose.translation().X(), bot_pose.translation().Y(), bot_pose.rotation().radians()] )
      
      draw_tag( best_result )


# Code relating to Webcam capture 

# Creates output window and initializes Webcam capture
def get_capture(window_name, video_capture_device_index=0):

    rickroll = "https://web.archive.org/web/2oe_/http://wayback-fakeurl.archive.org/yt/dQw4w9WgXcQ"
    localsim = "http://localhost:1181/?action=stream"
    roborio  = "http://roboRIO-3985-frc.local:1181/?action=stream" # IP depends on connection method (USB Tether, Ethernet, Radio)
    testfile = "tagtest.mp4"
    # Create a window named 'window_name'
    cv2.namedWindow(window_name)
    # Open the Webcam
    # For a usb camera provide port number
    # For a stream provide the URL of the video feed
    #cap = cv2.VideoCapture(video_capture_device_index)
    cap = cv2.VideoCapture(localsim)
    #if cap.isOpened():
        #print( "opened successfully" )
    network_table_instance.startClient4( "April Tag Processor" )
    network_table_instance.setServer( "localhost" )
    #network_table_instance.startDSClient()
    return cap

# Draws a "targeting overlay" on `frame`
def draw_overlay():
    # Get the height and width of the frame
    height, width, channels = frame.shape
    # Draw a circle in the center of the frame
    cv2.circle(frame, (width // 2, height // 2), 50, (0, 0, 255), 1)
    # Draw diagonal lines from top-left to bottom-right and top-right to bottom-left
    cv2.line(frame, (0, 0), (width, height), (0, 255, 0), 1)
    cv2.line(frame, (width, 0), (0, height), (0, 255, 0), 1)
    # Draw a text on the frame
    cv2.putText(frame, 'q to quit', (width//2 - 100, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Display loop: captures a frame, detects apriltags, draws an overlay, shows the composited frame
# Infinite loop breaks when user presses 'q' key on keyboard
def show_capture(capture_window_name, capture, detector, estimator):
  while True:
    # Capture frame-by-frame
    global frame
    ret, frame = capture.read()
    if frame is not None:
        # Detect apriltag, frame will be modified
        detect_and_process_apriltag( detector, estimator )
        draw_overlay()
        # Display the resulting frame in the named window
        cv2.imshow(capture_window_name, frame)
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Called once at program end
def cleanup_capture(capture):
    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()
    # Stop publishing to network tables
    bot_pose_pub.close()

# Main function:
# Initializes capture & display window, initializes Apriltag detection, shows capture, cleans up
def main():
    capture_window_name = 'Capture Window'
    capture = get_capture(capture_window_name, 0)

    """
    # Print field geometry and tag locations
    print( f"length: {field.getFieldLength()}" )
    print( f"width:  {field.getFieldWidth()}" )
    print( f"origin: {field.getOrigin()}" )
    i = 1
    while i <= 16:
        print( f"tag {i}: {field.getTagPose(i)}" )
        i += 1
    """

    detector, estimator = get_apriltag_detector_and_estimator( 640, 480 )

    # Loop while processing images.
    show_capture(capture_window_name, capture, detector, estimator)

    cleanup_capture(capture)

if __name__ == '__main__':
    main()
    # frame = cv2.imread('../frc_image.png')
    # assert frame is not None
    # detector, estimator = get_apriltag_detector_and_estimator((640,480))
    # out_frame = detect_and_process_apriltag(frame, detector, estimator)
    # cv2.imwrite('out.jpg', out_frame)