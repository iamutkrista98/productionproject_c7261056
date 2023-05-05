import cv2


def motiondetect():
    capture = cv2.VideoCapture(0)

    while True:
        _, frame1 = capture.read()
        _, frame2 = capture.read()

        difference = cv2.absdiff(frame2, frame1)
        difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

        difference = cv2.blur(difference, (5, 5))
        _, thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)

        contr, _ = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contr) > 0:
            max_cnt = max(contr, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "MOTION DETECTED", (10, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)

        else:
            cv2.putText(frame1, "NO MOTION DETECTED", (10, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)

        cv2.imshow("Motion Detection Mode", frame1)

        if cv2.waitKey(1) == 27:
            capture.release()
            cv2.destroyAllWindows()
            break
