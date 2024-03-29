# importing of all necessary libraries and functions
import cv2
from push_notification import push_notify
from event_logging import event_trigger
import time
# notification interval for sending in push notification set to 45 seconds to avoid flooding and performance issues during realtime frame capturing
notification_interval = 20
# all necessary variables declared and initialized
selectleft = False
selectright = False
x1, y1, x2, y2 = 0, 0, 0, 0


# select function with arguments as event x-axis , y-axis, the flag and necessary parameters
def selectregion(event, x, y, flag, parameter):
    # global variables declarations
    global x1, x2, y1, y2, selectleft, selectright
    # when the leftbutton of the mouse is put down as event then set the variable as necessary and put the coordinate over at that point
    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        selectleft = True
    # when the rightbutton of the mouse is put down as event then set the variable as necessary and put the coordinate over at that point
    elif event == cv2.EVENT_RBUTTONDOWN:
        x2, y2 = x, y
        selectright = True
        print(selectright, selectleft)
        print("Designated Area Set!")
        # the overall function above sets the region bounded by the point clicked on left side to the diagonal clicked over through the right mouse button

# main function for the designated boundary area motion detection


def designate():
    event_trigger('Designated Area Motion Detection Mode Initiated!')
    # global variable assignment
    global x1, x2, y1, y2, selectleft, selectright
    capture = cv2.VideoCapture(0)

    cv2.namedWindow("Designated Motion")
    # call the function to select region on mouse event
    cv2.setMouseCallback("Designated Motion", selectregion)
    last_notification_time = time.time()

    while True:
        _, frame = capture.read()

        cv2.imshow("Designated Motion", frame)

        if cv2.waitKey(1) == 27 or selectright == True:
            cv2.destroyAllWindows()
            break

    while True:
        # frame1 reading through the capture
        _, frame1 = capture.read()
        # frame2 captured
        _, frame2 = capture.read()

        # exclusive frame1 assignment of respective axioms
        frame1only = frame1[y1:y2, x1:x2]
        # exclusive frame2 assignment of respective axioms
        frame2only = frame2[y1:y2, x1:x2]

        # evaluation of difference between two exclusive frames
        difference = cv2.absdiff(frame2only, frame1only)
        # convert into grayscale
        difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

        # introduce blur for processing
        difference = cv2.blur(difference, (5, 5))
        # threshold introduction for removing noise
        _, thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)

        # identifying of contours or fine edges within the processed image
        contr, _ = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # if detection of contours as anomaly, it is believed that motion has occured
        if len(contr) > 0:
            max_cnt = max(contr, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame1, (x+x1, y+y1),
                          (x+w+x1, y+h+y1), (0, 255, 0), 2)
            cv2.putText(frame1, "MOTION DETECTED", (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            current_time = time.time()
            if current_time-last_notification_time >= notification_interval:
                push_notify('Motion Detected in Designated Location! Alert!')
            else:
                print('')
        # else condition when contour not identified
        else:
            cv2.putText(frame1, "NO MOTION DETECTED", (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.rectangle(frame1, (x1, y1), (x2, y2), (0, 0, 255), 1)
        cv2.imshow("Designated Motion", frame1)

        # exit out of mode condition active on pressing esc key
        if cv2.waitKey(1) == 27:
            capture.release()
            cv2.destroyAllWindows()
            selectleft = False
            selectright = False
            x1, y1, x2, y2 = 0, 0, 0, 0
            event_trigger('Designated Area Motion Detection Session Ended!')

            break
