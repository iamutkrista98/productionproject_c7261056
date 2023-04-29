# importing of package
import cv2
# importing date and time
from datetime import datetime

# function to record


def live():
    # give the camera source for capture, here for now default source provided with index
    cap = cv2.VideoCapture(1)
    while True:
        # reading the frames till condition is true that means continuously
        _, frame = cap.read()
        # put the text on the screen for monitoring purpose and live view while being recorded in background
        cv2.putText(frame, f'{datetime.now().strftime("%D-%H-%M-%S")}', (50, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    0.5, (255, 255, 255), 2)
        # set the frame title to live monitoring mode
        cv2.imshow("Live Monitoring Mode", frame)

        # condition to close the current frame
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            break
