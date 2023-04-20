# importing of package
import cv2

# default camera source
cap = cv2.VideoCapture(0)

# writing to disk giving all the necessary specification of type, framerate and resolution
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# execution till it is receiving the live image frames from the designated camera
while True:
    _, frame = cap.read()

    out.write(frame)

    # title information
    cv2.imshow("live footage", frame)

    # logic for quitting the program function
    if cv2.waitKey(1) == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
