import cv2
import time
import numpy as np
from datetime import datetime
from theftdetection import theftdetection

def find_motion():
    motion_detected = False
    is_start_done = False
    cap = cv2.VideoCapture(0)

    check = []
    print("Waiting for 2 seconds...")
    time.sleep(2)
    _, frame1 = cap.read()

    frm1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    while True:
        _, frame2 = cap.read()  # Properly retrieve frame2
        frm2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frm1, frm2)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if cv2.contourArea(c) > 25]

        if len(contours) > 5:
            cv2.putText(thresh, "Motion Suspected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            motion_detected = True
            is_start_done = False

        elif motion_detected and len(contours) < 3:
            if not is_start_done:
                start = time.time()
                is_start_done = True
                end = time.time()

            end = time.time()
            print(end - start)
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
        else:
            cv2.putText(thresh, "No Motion Suspected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

        cv2.imshow("Find Motion Mode", thresh)

        _, frm1 = cap.read()
        frm1 = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY)

        if cv2.waitKey(1) == 27:
            break

    return
