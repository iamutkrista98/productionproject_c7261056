# importing of all the necessary libraries and packages
import cv2
import os
from datetime import datetime


# function for inout detection
def in_out_detection():
    # create directory if not exist
    visitors_directory = 'visitors'
    if not os.path.exists(visitors_directory):
        os.mkdir(visitors_directory)
    in_directory = 'visitors/in'
    if not os.path.exists(in_directory):
        os.mkdir(in_directory)
    out_directory = 'visitors/out'
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)
    capture = cv2.VideoCapture(0)
    right, left = "", ""

    while True:
        _, frame1 = capture.read()
        frame1 = cv2.flip(frame1, 1)
        _, frame2 = capture.read()
        frame2 = cv2.flip(frame2, 1)
        # evaluating the absolute difference between the two frames
        difference = cv2.absdiff(frame2, frame1)
        # smoothening the image using kernal distance
        difference = cv2.blur(difference, (5, 5))
        # convert the feed received into grayscale
        gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        # getting bi level image out of threshold image applying fix level thresholding to array element
        _, threshd = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
        # detecting the edge details or the contours detected within the thresholded frame obtained
        contr, _ = cv2.findContours(
            threshd, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        x = 300
        if len(contr) > 0:
            max_cnt = max(contr, key=cv2.contourArea)
            # drawing rectangle over the contour detected area and bounding it
            x, y, w, h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "MOTION DETECTED", (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # for right movement from camera screen, movement greater than 500 in the x axis
        if right == "" and left == "":
            if x > 500:
                right = True
            elif x < 200:
                left = True
        elif right:
            if x < 200:
                print("movement to left")
                x = 300
                # initialize the values again
                right, left = "", ""
                # writing the frame snap image to disk under visitor in folder with proper timestamp
                cv2.imwrite(
                    f"visitors/in/{datetime.now().strftime('%y-%m-%d-%H-%M-%S')}.jpg", frame1)
        # for movement in the left direction in the x-axis plane
        elif left:
            if x > 500:
                print("movement to right")
                x = 300
                # reinitialize the position markings
                right, left = "", ""
                # writing the frame snap image to disk under visitor out folder with proper timestamp
            cv2.imwrite(
                f"visitors/out/{datetime.now().strftime('%y-%m-%d-%H-%M-%S')}.jpg", frame1)
        cv2.imshow("In Out Detection Mode", frame1)
        # waiting for input key and exit logic
        k = cv2.waitKey(1)

        if (k == 27):
            capture.release()
            cv2.destroyAllWindows()
            break
