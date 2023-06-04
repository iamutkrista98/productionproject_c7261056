# importing of necessary libraries and functions
import cv2
import time
import numpy as np
from datetime import datetime
from theftdetection import theftdetection

# finding motion function for theft structural similarity scenario


def find_motion():
    # setting of initial boolean status for motions
    motion_detected = False
    is_start_done = False
    # capture assigned to first indexed camera interfaced to computer
    cap = cv2.VideoCapture(0)

    check = []
    # wait for two seconds and evaluate the surrounding and capture a frame
    print("Waiting for 2 seconds...")
    time.sleep(2)
    _, frame1 = cap.read()
    # converting to grayscale
    frm1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    # capture till condition met continouously
    while True:
        _, frame2 = cap.read()  # Properly retrieve frame2
        frm2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frm1, frm2)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if cv2.contourArea(c) > 25]
        # when identified countours or edges greater than 5
        if len(contours) > 5:
            cv2.putText(thresh, "Motion Suspected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            motion_detected = True
            is_start_done = False
        # when motion detected identified as true and contours at least less than 3
        elif motion_detected and len(contours) < 3:
            if not is_start_done:
                start = time.time()
                is_start_done = True
                end = time.time()
            # assign end time as current time
            end = time.time()
            # printing of time difference
            print(end - start)
            # if the time difference between the end and start of mocap is greater than 4
            if (end - start) > 4:
                cap.release()
                cv2.destroyAllWindows()
                print("frame1 shape:", frame1.shape)
                print("frame2 shape:", frame2.shape)  # Check shape of frame2
                x = theftdetection(frame1, frame2)
                if x == 0:
                    print("Running Again")
                    return
                else:
                    print("Found Motion")

                    return
        # when no motion has been suspected and no flags set
        else:
            cv2.putText(thresh, "No Motion Suspected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

        cv2.imshow("Find Motion Mode", thresh)
        # recapture the frame
        _, frm1 = cap.read()
        frm1 = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY)

        if cv2.waitKey(1) == 27:
            break

    return
