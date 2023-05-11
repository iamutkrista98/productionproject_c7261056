import cv2

"""
def theftdetection():
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # Read the initial frame
    ret, frame1 = cap.read()

    # Convert frame to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # Set up the background subtractor
    fgbg = cv2.createBackgroundSubtractorMOG2()

    while True:
        # Read the current frame
        ret, frame2 = cap.read()
        
        # Convert frame to grayscale
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Perform background subtraction
        fgmask = fgbg.apply(gray2)
        
        # Apply thresholding to obtain binary image
        _, thresh = cv2.threshold(fgmask, 30, 255, cv2.THRESH_BINARY)
        
        # Apply morphological operations to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Find contours of the objects in the image
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Ignore small contours
            if cv2.contourArea(contour) < 1000:
                continue
            
            # Draw bounding rectangle around the contour
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame2, 'Theft Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('Theft Detection', frame2)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close the windows
    cap.release()
    cv2.destroyAllWindows() 

    """
#importing of necessary libraries and packages
import cv2
import time
from skimage.metrics import structural_similarity
from datetime import datetime


# import beepy

def theftdetection(frame1, frame2):
    frame1 = frame1[1]
    frame2 = frame2[1]

    g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    g1 = cv2.blur(g1, (2, 2))
    g2 = cv2.blur(g2, (2, 2))

    (score, diff) = structural_similarity(g2, g1, full=True)

    print("Image Similarity", score)

    diff = (diff * 255).astype("uint8")
    thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY_INV)[1]

    contors = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contors = [c for c in contors if cv2.contourArea(c) > 50]

    if len(contors):
        for c in contors:
            x, y, w, h = cv2.boundingRect(c)

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    else:
        print("nothing stolen")
        return 0

    cv2.imshow("Difference Threshold", thresh)
    cv2.imshow("Detailed", frame1)
    cv2.imwrite("stolen/" + datetime.now().strftime('%y-%m-%d-%H-%M-%S') + ".png", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return 1
