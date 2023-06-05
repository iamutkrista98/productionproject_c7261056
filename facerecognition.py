# importing of all the necessary libraries and functions for the requirement fulfilment domain
import cv2
import os
import numpy as np
import tkinter as tk
import tkinter.font as font
import easygui as easygui
from push_notification import push_notify
from event_logging import event_trigger
import time
import ctypes
# notification interval for sending in push notification set to 45 seconds to avoid flooding and performance issues during realtime frame capturing
notification_interval = 20

# function to collect face based data and storing into disk based on name and id supplied


def data_collection():

    # create directory if not exist for facesamples collected during the training processing
    facesamples_directory = 'facesamples'
    if not os.path.exists(facesamples_directory):
        os.mkdir(facesamples_directory)
    # gui element to get name and id
    optiontitle="Input Details"
    fields=["Enter Name: ","Provide an ID: "]
    input_values=easygui.multenterbox("Enter the required information",optiontitle,fields)

    if input_values is None:
        print('Operation Cancelled')
    else:
        count = 1
        name,id=input_values
        #name = easygui.enterbox("Enter name: ")
        
        #id = easygui.enterbox("Enter id: ")
        # selecting the camera source
        capture = cv2.VideoCapture(0)
        # loading the haarcascade frontal face classifier
        classifier = "haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(classifier)
        # till the condition is met
        while True:
            # capturing of frame
            _, framecapture = capture.read()
            gray = cv2.cvtColor(framecapture, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(gray, 1.4, 1)
            # looping through face dimensional elements the axioms, width, height etc
            for x, y, w, h in faces:
                cv2.rectangle(framecapture, (x, y), (x+w, y+h), (0, 255, 0), 2)
                roi = gray[y:y+h, x:x+w]
                #writing the captured images with the format name-image count no till 201-id assigned
                cv2.imwrite(f"facesamples/{name}-{count}-{id}.jpg", roi)

                count = count+1
                # putting the the text as visualization over the screen window
                cv2.putText(framecapture, f"{count}", (20, 20),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                cv2.imshow("New Face Enrollment", roi)
            # open the frame within the new window
            cv2.imshow("Identification Window", framecapture)
            # exit conditions for the training faces functionality whereby the window exits on capturing 200 face samples
            if cv2.waitKey(1) == 27 or count > 200:
                cv2.destroyAllWindows()
                capture.release()
                training_faces()
                break

# function to train unknown faces and updating the training model


def training_faces():
    print("Face Training Function Initialized")
    # instantiate the LBPHFaceRecognizer for face recognitition
    recognize = cv2.face.LBPHFaceRecognizer_create()
    # provide the dataset location for collection
    dataset = 'facesamples'
    paths = [os.path.join(dataset, images) for images in os.listdir(dataset)]
    # initialization of different array based variables requisites
    faces = []
    id = []
    label = []
    for path in paths:
        label.append(path.split('/')[-1].split('-')[0])
        id.append(int(path.split('/')[-1].split('-')[2].split('.')[0]))
        faces.append(cv2.imread(path, 0))
    # store the extracted features in the form of array corresponding to the id supplied
    recognize.train(faces, np.array(id))
    # save the training model with the data collected in the form of array elements through feature extraction from faces during the training phase
    recognize.save('trainingmodel.yml')
    print("Training Model Saved and Updated to Disk!")
    event_trigger('New Face Data Enrolled and Training Model Updated!')

    return

# function for recognition of known faces that have already been inputted to disk


def facerecognition():
    event_trigger('Face Identification Mode Initialized!')
    capture = cv2.VideoCapture(0)
    # loading of the haarcascade frontal face identifying classifier
    filename = "haarcascade_frontalface_default.xml"
    # path where the facesamples were stored during the training phase
    paths = [os.path.join("facesamples", images)
             for images in os.listdir("facesamples")]
    labelslist = {}
    for path in paths:
        labelslist[path.split('/')[-1].split('-')[2].split('.')
                   [0]] = path.split('/')[-1].split('-')[0]
    print(labelslist)
    recognize = cv2.face.LBPHFaceRecognizer_create()
    # reading the trainingmodel file whereby the data features were collected
    recognize.read('trainingmodel.yml')
    cascade = cv2.CascadeClassifier(filename)

    last_notification_time = time.time()
    # the condition to loop till
    while True:
        _, framecapture = capture.read()
        gray = cv2.cvtColor(framecapture, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.3, 2)

        for x, y, w, h in faces:
            cv2.rectangle(framecapture, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi = gray[y:y+h, x:x+w]
            label = recognize.predict(roi)

            if label[1] < 100:
                cv2.putText(framecapture, f"{labelslist[str(label[0])]}",
                            (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            else:
                # if the visitor identified within the frame is not recognized based on the data collected prior during the training phase
                cv2.putText(framecapture, "Unknown Face", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                current_time = time.time()
                if current_time-last_notification_time >= notification_interval:
                    push_notify('Unidentified visitor in frame ')
                    last_notification_time = current_time
        cv2.imshow("Identification", framecapture)
        # window closing condition
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            capture.release()
            event_trigger('Face Identification Mode Exited!')

            break

# main function for arrangement of seperate gui element for multiple functionalities to be integrated in the identification functionality


def maincall():
    event_trigger('Face Identification Mode Initialized!')
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.geometry("470x200")
    root.minsize(470, 200)
    root.maxsize(470, 200)

    # getting the current screen resolution
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # evaluating the center position
    xpos = (screen_width/2)-(470/2)
    ypos = (screen_height/2)-(200/2)

    root.geometry("+%d+%d" % (xpos, ypos))

    root.title("Identification")
    root.iconbitmap('icons/face.ico')

    label = tk.Label(root, text="Select an Option")
    label.grid(row=0, columnspan=2)
    label_font = font.Font(size=35, weight='bold', family='Courier-New')
    label['font'] = label_font

    btn_font = font.Font(size=22)

    button1 = tk.Button(root, text="Train New", bg='lime', fg='black',
                        command=data_collection, height=2, width=20)
    button1.grid(row=1, column=0, pady=(10, 10), padx=(5, 5))
    button1['font'] = btn_font

    button2 = tk.Button(root, text="Identify Known", bg='orange', fg='black',
                        command=facerecognition, height=2, width=20)
    button2.grid(row=1, column=1, pady=(10, 10), padx=(5, 5))
    button2['font'] = btn_font

    button3 = tk.Button(root, text="Exit",
                        command=root.destroy, height=2, width=20, bg='red', fg='black')
    button3.grid(row=2, column=0, pady=(10, 10), padx=(5, 5), columnspan=2)
    button3['font'] = btn_font
    root.mainloop()
    return
