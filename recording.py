# importing the opencv module
import cv2
import os
# importing date and time for footage writing with timestamps
from datetime import datetime
from push_notification import push_notify
from event_logging import event_trigger
import winsound
frequency = 2500
duration = 2000

# function to record


def record():
    event_trigger('Recording Functionality Started!')
    # create directory if not exist
    recording_directory = 'footages'
    if not os.path.exists(recording_directory):
        os.mkdir(recording_directory)
    # give the camera source for capture, here for now default source provided with index
    cap = cv2.VideoCapture(0)
    # getting the current camera interfaced frame width, height and fps
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(frameHeight)
    print(frameWidth)
    print(fps)
    print(n_frames)

    # provide the format of the footage file which will be written to disk
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # configuration of outputted video footage to write to disk providing date and time with mp4 extension as file name and record in 30 fps and native resolution of interfaced camera
    out = cv2.VideoWriter(
        f'footages/{datetime.now().strftime("%y-%m-%d-%H-%M-%S")}.mp4', fourcc, 30, (frameWidth, frameHeight))
    event_trigger('Recording footage saved to disk!')

    while True:
        # reading the frames till condition is true that means continuously
        _, frame = cap.read()
        # put the text on the screen for monitoring purpose and live view while being recorded in background
        cv2.putText(frame, 'Rec: '+f'{datetime.now().strftime("%y-%m-%d-%H-%M-%S")}', (50, 50), cv2.FONT_HERSHEY_DUPLEX,
                    1.0, (0, 0, 255), 2)

        out.write(frame)
        # set the frame title to recording mode
        cv2.imshow("Recording Mode", frame)

        # condition to close the current frame
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            event_trigger('Recording Stopped!')
            # winsound.Beep(frequency,duration)
            break
