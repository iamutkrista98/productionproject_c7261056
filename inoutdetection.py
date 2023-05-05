import cv2
from datetime import datetime


#function for inout detection 
def in_out_detection():
    capture = cv2.VideoCapture(0)
    right, left = "",""

    while True:
        _, frame1 = capture.read()
        frame1 = cv2.flip(frame1,1)
        _,frame2 = capture.read()
        frame2 = cv2.flip(frame2,1)


        difference = cv2.absdiff(frame2,frame1)
        #smoothening the image using kernal distance
        difference = cv2.blur(difference,(5,5))
        #convert the feed received into grayscale
        gray = cv2.cvtColor(difference,cv2.COLOR_BGR2GRAY)
        #getting bi level image out of threshold image applying fix level thresholding to array element 
        _, threshd = cv2.threshold(gray,40,255,cv2.THRESH_BINARY)

        contr,_ = cv2.findContours(threshd,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        x=300
        if len(contr)>0:
            max_cnt = max(contr, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame1,"MOTION DETECTED",(10,80),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)


        #for right movement from camera screen
        if right=="" and left=="":
            if x>500:
                right=True
            elif x<200:
                left=True 
        elif right:
            if x<200:
                print("movement to left")
                x=300
                #initialize the values again
                right,left="",""
                #writing the frame snap image to disk under visitor in folder with proper timestamp
                cv2.imwrite(f"visitors/in/{datetime.now().strftime('%y-%m-%d-%H-%M-%S')}.jpg",frame1)

        elif left:
                if x>500:
                    print("movement to right")
                    x=300
                    #reinitialize the position markings
                    right,left="",""
                     #writing the frame snap image to disk under visitor out folder with proper timestamp
                cv2.imwrite(f"visitors/out/{datetime.now().strftime('%y-%m-%d-%H-%M-%S')}.jpg",frame1)
        cv2.imshow("In Out Detection Mode",frame1)

        k=cv2.waitKey(1)

        if(k==27):
            capture.release()
            cv2.destroyAllWindows()
            break








