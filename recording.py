# importing the opencv module
import cv2
# importing date and time
from datetime import datetime

# function to record


def record():
    # give the camera source for capture, here for now default source provided with index
    cap = cv2.VideoCapture(1)

    # provide the format of the footage file which will be written to disk
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # configuration of outputted video footage to write to disk providing date and time with mp4 extension as file name and record in 30 fps and resolution 640*480
    out = cv2.VideoWriter(
        f'recordings/{datetime.now().strftime("%H-%M-%S")}.mp4', fourcc, 30.0, (640, 480))

    while True:
        # reading the frames till condition is true that means continuously
        _, frame = cap.read()
        # put the text on the screen for monitoring purpose and live view while being recorded in background
        cv2.putText(frame, f'{datetime.now().strftime("%D-%H-%M-%S")}', (50, 50), cv2.FONT_HERSHEY_COMPLEX,
                    0.6, (255, 255, 255), 2)

        out.write(frame)
        # set the frame title to recording mode
        cv2.imshow("Recording Mode", frame)

        # condition to close the current frame
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            break
