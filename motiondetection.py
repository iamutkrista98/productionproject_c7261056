# importing of necessary libraries and functions
import cv2
from event_logging import event_trigger
# function for motion detection functionality


def motiondetect():
    event_trigger('Motion Detection Mode Initialized!')
    # selection of the camera source feeding
    capture = cv2.VideoCapture(0)

    while True:
        # capturing of two consecutive frames
        _, frame1 = capture.read()
        _, frame2 = capture.read()
        # measuring the absolute difference between the two frames captured
        difference = cv2.absdiff(frame2, frame1)
        # apply grayscale to the difference frame evaluated
        difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        # apply blur as processing to the frame difference identified
        difference = cv2.blur(difference, (5, 5))
        # threshold application to the difference frame evaluated
        _, thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        # finding countours identified within the thresholded frame
        contr, _ = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # motion detection identified when contour identified
        if len(contr) > 0:
            max_cnt = max(contr, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "MOTION DETECTED", (5, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        else:
            cv2.putText(frame1, "NO MOTION DETECTED", (10, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # displaying the mode within the given frame
        cv2.imshow("Motion Detection Mode", frame1)

        # exit mode logic
        if cv2.waitKey(1) == 27:
            capture.release()
            cv2.destroyAllWindows()
            event_trigger('Motion Detection Mode Suspended!')

            break
