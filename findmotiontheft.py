import cv2
from theftdetection import theftdetection
import time
import numpy as np

#find motion functionality
def find_motion():
    #necessary variables declared for boolean initialized as False
    motion_detected = False
    is_start_done = False
    #capture from the defined source
    cap = cv2.VideoCapture(0)

    check = []
    #wait for 5 seconds to analyze the current state and capture the frame 
    print("waiting for 2 seconds")
    time.sleep(2)
    frame1 = cap.read()

    _, frm1 = cap.read()
    frm1 = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY)

    while True:
        _, frm2 = cap.read()
        frm2 = cv2.cvtColor(frm2, cv2.COLOR_BGR2GRAY)
        #frame difference evaluation 
        diff = cv2.absdiff(frm1, frm2)
        #thresholding of difference in frame processed
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        #for identification of contours in the threshold applied frame
        contors = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        # look at it
        contors = [c for c in contors if cv2.contourArea(c) > 25]
        #when contour is more than 5 
        if len(contors) > 5:
            cv2.putText(thresh, "Motion Suspected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            motion_detected = True
            is_start_done = False
        #adjustment of initialized variables accordingly to the number of contours identified
        elif motion_detected and len(contors) < 3:
            if is_start_done == False:
                start = time.time()
                is_start_done = True
                end = time.time()

            end = time.time()

            #start time and end time difference
            print(end - start)
            if (end - start) > 4:
                frame2 = cap.read()
                cap.release()
                cv2.destroyAllWindows()
                x = theftdetection(frame1, frame2)
                if x == 0:
                    print("Running Again")
                    return

                else:
                    print("Found Motion")
                    return

        else:
            cv2.putText(thresh, "No Motion Suspected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        #for output window inside of the given frame
        cv2.imshow("Find Motion Mode", thresh)

        _, frm1 = cap.read()
        frm1 = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY)
        
        if cv2.waitKey(1) == 27:
            break

    return