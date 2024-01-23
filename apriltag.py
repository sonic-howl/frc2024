# This is a quick demo of the apriltag detection and applying overlays
# to a webcam camera stream. Use as inspiration or reference for robot vision.
# original file: https://gist.github.com/lobrien/5d5e1b38e5fd64062c43ac752b74889c

import cv2
import robotpy_apriltag
import math

# This function is called once to initialize the apriltag detector and the pose estimator
def get_apriltag_detector_and_estimator( width: float, height: float ):
    detector = robotpy_apriltag.AprilTagDetector()
    # FRC 2024 uses tag36h11
    assert detector.addFamily("tag36h11")

    # Focal lengths need to be characterised for robot camera.
    tagSize = 6.5 * 0.0254 # 6.5 inches convert to meters
    # rough focal length measure using ruler as target.
    fx = width  * 14.5/12.0
    fy = height * 19.5/12.0
    estimator = robotpy_apriltag.AprilTagPoseEstimator(
    robotpy_apriltag.AprilTagPoseEstimator.Config(
            tagSize, fx, fy, width / 2.0, height / 2.0
        )
    )
    return detector, estimator
    
# This function is called for every detected tag. It uses the `estimator` to 
# return information about the tag, including its centerpoint. (The corners are 
# also available.)
def process_apriltag(estimator, tag):
    tag_id = tag.getId()
    center = tag.getCenter()
    hamming = tag.getHamming()
    decision_margin = tag.getDecisionMargin()
    #print("Hamming for {} is {} with decision margin {}".format(tag_id, hamming, decision_margin))

    est = estimator.estimateOrthogonalIteration(tag, 50)
    return tag_id, est.pose1, center

# This simply outputs some information about the results returned by `process_apriltag`.
# It prints some info to the console and draws a circle around the detected center of the tag
# Illustrates how you can add target reticles or other drive team aids to the camera view.
def draw_tag(frame, result):
    assert frame is not None
    assert result is not None
    tag_id, pose, center = result
    #print(center)
    cv2.circle(frame, (int(center.x), int(center.y)), 50, (255, 0, 255), 3)
    msg  = f"Tag ID: {tag_id}"
    msg2 = f"Center: {center}"
    msg3 = f"Pose T: {pose.translation()}"
    msg4 = f"Pose R: {pose.rotation()}"
    cv2.putText(frame, msg,  (150, 50 * 1), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 100), 2)
    cv2.putText(frame, msg2, ( 50, 50 * 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 100), 2)
    cv2.putText(frame, msg3, ( 50, 50 * 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 100), 2)
    cv2.putText(frame, msg4, ( 50, 50 * 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 100), 2)
    return frame

# This function is called once for every frame captured by the Webcam. For testing, it can simply
# be passed a frame capture loaded from a file. (See commented-out alternative `if __name__ == main:` at bottom of file)
def detect_and_process_apriltag(frame, detector, estimator):
    assert frame is not None
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect apriltag
    tag_info = detector.detect(gray)
    DETECTION_MARGIN_THRESHOLD = 100
    filter_tags = [tag for tag in tag_info if tag.getDecisionMargin() > DETECTION_MARGIN_THRESHOLD]
    results = [ process_apriltag(estimator, tag) for tag in filter_tags ]
    # Note that results will be empty if no apriltag is detected
    for result in results:
        frame = draw_tag(frame, result)
    return frame

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
    cap = cv2.VideoCapture(roborio)
    #if cap.isOpened():
        #print( "opened successfully" )
    return cap

# Draws a "targeting overlay" on `frame`
def draw_overlay(frame):
    # Get the height and width of the frame
    height, width, channels = frame.shape
    # Draw a circle in the center of the frame
    cv2.circle(frame, (width // 2, height // 2), 50, (0, 0, 255), 1)
    # Draw diagonal lines from top-left to bottom-right and top-right to bottom-left
    cv2.line(frame, (0, 0), (width, height), (0, 255, 0), 1)
    cv2.line(frame, (width, 0), (0, height), (0, 255, 0), 1)
    # Draw a text on the frame
    cv2.putText(frame, 'q to quit', (width//2 - 100, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return frame

# Display loop: captures a frame, detects apriltags, draws an overlay, shows the composited frame
# Infinite loop breaks when user presses 'q' key on keyboard
def show_capture(capture_window_name, capture, detector, estimator):
    while True:
        # Capture frame-by-frame
        ret, frame = capture.read()
        # Detect apriltag
        frame_with_maybe_apriltags = detect_and_process_apriltag(frame, detector, estimator)

        overlaid_image = draw_overlay(frame_with_maybe_apriltags)
        # Display the resulting frame in the named window
        cv2.imshow(capture_window_name, overlaid_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Called once at program end
def cleanup_capture(capture):
    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()

# Main function:
# Initializes capture & display window, initializes Apriltag detection, shows capture, cleans up
def main():
    capture_window_name = 'Capture Window'
    capture = get_capture(capture_window_name, 0)
    detector, estimator = get_apriltag_detector_and_estimator( 640, 480 )
    show_capture(capture_window_name, capture, detector, estimator)
    cleanup_capture(capture)

if __name__ == '__main__':
    main()
    # frame = cv2.imread('../frc_image.png')
    # assert frame is not None
    # detector, estimator = get_apriltag_detector_and_estimator((640,480))
    # out_frame = detect_and_process_apriltag(frame, detector, estimator)
    # cv2.imwrite('out.jpg', out_frame)