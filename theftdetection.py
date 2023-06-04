# importing of necessary libraries, packages and functions
import cv2
import time
from skimage.metrics import structural_similarity
from datetime import datetime
from event_logging import event_trigger
import os


def theftdetection(frame1, frame2):
    event_trigger('Monitoring Functionality Started!')
    # create directory if not exist
    monitoring_directory = 'stolen'
    if not os.path.exists(monitoring_directory):
        os.mkdir(monitoring_directory)

    # conversion into grayscale for both frames
    grayscale1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    grayscale2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # applying blur as part of image processing on the two frames
    grayscale1 = cv2.blur(grayscale1, (2, 2))
    grayscale2 = cv2.blur(grayscale2, (2, 2))
    # evaluate structural similarity score between the two grayscaled frames
    (score, diff) = structural_similarity(grayscale2, grayscale1, full=True)
    # printing the similarity score
    print("Image similarity:", score)
    # defining the datatype for the differential score evaluated
    diff = (diff * 255).astype("uint8")
    # removal of unnecessary noises through threshold application on the differential frame
    thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # find edges or contours from the thresholded frame
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv2.contourArea(c) > 50]
    # condition for till contours are identified
    if len(contours):
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        print("Nothing stolen")
        return 0
    # view the different frames consisting of relevant frames
    cv2.imshow("Difference", thresh)
    # cv2.imshow("Frame1", frame1)
    cv2.imshow("Frame2", frame2)
    # writing the frame 2 image to disk in the appropriate directory
    cv2.imwrite(
        "stolen/" + datetime.now().strftime("%y-%m-%d-%H-%M-%S") + ".jpg", frame2)
    event_trigger('Monitoring Functionality Session Ended!')

    # exit logic
    cv2.waitKey(0)
    cv2.destroyAllWindows()
