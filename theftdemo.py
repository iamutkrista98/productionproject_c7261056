import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def theftdemo():
    # Define the path to the reference image of the scene without any theft
    reference_image_path = "reference.jpg"
    video_path = "theft1.mp4"

    # Load the reference image
    reference_image = cv2.imread(reference_image_path, 0)  # Load as grayscale

    # Define the minimum similarity score threshold for theft detection
    similarity_threshold = 0.9

    # Get the dimensions of the reference image
    reference_height, reference_width = reference_image.shape[:2]

    # Initialize the video capture object
    video = cv2.VideoCapture(video_path)

    # Set up the object tracker
    object_tracker = cv2.TrackerCSRT_create()

    # Read the first frame from the video
    _, frame = video.read()

    # Resize the frame to match the dimensions of the reference image
    frame = cv2.resize(frame, (reference_width, reference_height))

    # Initialize the object bounding box
    object_bbox = None

    # Convert the first frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Compute the similarity between the reference image and the first frame
    similarity_score = ssim(reference_image, frame_gray, full=True)

    # Main loop
    while True:
        # Read a new frame from the video
        _, frame = video.read()

        # If the frame is not successfully read, end the loop
        if frame is None:
            break

        # Resize the frame to match the dimensions of the reference image
        frame = cv2.resize(frame, (reference_width, reference_height))

        # Convert the frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute the similarity between the reference image and the current frame
        similarity_score = ssim(reference_image, frame_gray, full=True)

        # Extract the similarity score value from the tuple
        similarity_score = similarity_score[0]

        # Calculate the average similarity score
        avg_similarity_score = np.mean(similarity_score)

        # If the average similarity score is below the threshold, theft is detected
        if avg_similarity_score < similarity_threshold:
            # Initialize the object tracker with the first frame and the initial bounding box
            object_bbox = cv2.selectROI(
                "Object Tracker", frame, fromCenter=False, showCrosshair=True)
            object_tracker.init(frame, object_bbox)

            # Take a snapshot after theft is detected and save it to the disk
            snapshot = frame.copy()
            marked_object = frame[object_bbox[1]:object_bbox[1] +
                                  object_bbox[3], object_bbox[0]:object_bbox[0]+object_bbox[2]]
            cv2.imwrite("theft_snapshot.jpg", snapshot)
            cv2.imwrite("stolen_object.jpg", marked_object)
            break

    # Create a window to display the video feed
    cv2.namedWindow("Video Feed", cv2.WINDOW_NORMAL)

    # Main loop for object tracking
    while True:
        # Read a new frame from the video
        _, frame = video.read()

        # If the frame is not successfully read, end the loop
        if frame is None:
            break

        # Resize the frame to match the dimensions of the reference image
        frame = cv2.resize(frame, (reference_width, reference_height))

        # Update the object tracker
        success, bbox = object_tracker.update(frame)

        # If tracking is successful, draw the bounding box around the object
        if success:
            # Convert the object bounding box coordinates to integers
            bbox = tuple(map(int, bbox))

            # Draw the bounding box rectangle
            cv2.rectangle(frame, bbox, (0, 255, 0), 2)

        # Display the frame with the bounding box
        cv2.imshow("Video Feed", frame)

        # Check for user key press
        key = cv2.waitKey(1) & 0xFF

        # If the 'q' key is pressed, exit the loop
        if key == ord("q"):
            break

    # Release the video capture object and close all windows
    video.release()
    cv2.destroyAllWindows()
