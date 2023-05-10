import cv2
import os
import numpy as np
import tkinter as tk
import tkinter.font as font
import easygui as easygui

#function to collect face based data and storing into disk based on name and id supplied 
def data_collection():

    #create directory if not exist
    facesamples_directory='facesamples'
    if not os.path.exists(facesamples_directory):
        os.mkdir(facesamples_directory)

    name = easygui.enterbox("Enter name: ")
    count = 1
    id = easygui.enterbox("Enter id: ")
    capture = cv2.VideoCapture(0)
    classifier = "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(classifier)

    while True:
        _, framecapture = capture.read()
        gray = cv2.cvtColor(framecapture, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.4, 1)

        for x, y, w, h in faces:
            cv2.rectangle(framecapture, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi = gray[y:y+h, x:x+w]
            cv2.imwrite(f"facesamples/{name}-{count}-{id}.jpg", roi)
            count = count+1
            cv2.putText(framecapture, f"{count}", (20, 20),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
            cv2.imshow("New Enrollment", roi)

        cv2.imshow("Identification Window", framecapture)

        if cv2.waitKey(1) == 27 or count > 200:
            cv2.destroyAllWindows()
            capture.release()
            training_faces()
            break

#function to train unknown faces and updating the training model
def training_faces():
    print("Face Training Function Initialized")
    recognize = cv2.face.LBPHFaceRecognizer_create()
    dataset = 'facesamples'
    paths = [os.path.join(dataset, images) for images in os.listdir(dataset)]
    faces = []
    id = []
    label = []
    for path in paths:
        label.append(path.split('/')[-1].split('-')[0])
        id.append(int(path.split('/')[-1].split('-')[2].split('.')[0]))
        faces.append(cv2.imread(path, 0))

    recognize.train(faces, np.array(id))
    recognize.save('trainingmodel.yml')
    print("Training Model Saved and Updated to Disk!")
    return

#function for recognition of known faces that have already been inputted to disk
def facerecognition():
    capture = cv2.VideoCapture(0)
    filename = "haarcascade_frontalface_default.xml"

    paths = [os.path.join("facesamples", images)
             for images in os.listdir("facesamples")]
    labelslist = {}
    for path in paths:
        labelslist[path.split('/')[-1].split('-')[2].split('.')
                   [0]] = path.split('/')[-1].split('-')[0]
    print(labelslist)
    recognize = cv2.face.LBPHFaceRecognizer_create()
    recognize.read('trainingmodel.yml')
    cascade = cv2.CascadeClassifier(filename)

    while True:
        _, framecapture = capture.read()
        gray = cv2.cvtColor(framecapture, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.3, 2)

        for x, y, w, h in faces:
            cv2.rectangle(framecapture, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi = gray[y:y+h, x:x+w]
            label = recognize.predict(roi)

            if label[1] < 100:
                cv2.putText(framecapture, f"{labelslist[str(label[0])]}+{int(label[1])}",
                            (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            else:
                cv2.putText(framecapture, "Unknown Face", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.imshow("Identification", framecapture)

        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            capture.release()
            break

#main function for arrangement of seperate gui element for multiple functionalities to be integrated
def maincall():
    root = tk.Tk()
    root.geometry("400x200")
    root.minsize(400, 200)
    root.maxsize(400, 200)

    #getting the current screen resolution 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    #evaluating the center position 
    xpos=(screen_width/2)-(400/2)
    ypos=(screen_height/2)-(200/2)

    root.geometry("+%d+%d" %(xpos,ypos))

    root.title("Identification")

    label = tk.Label(root, text="Select an Option from below Buttons ")
    label.grid(row=0, columnspan=2)
    label_font = font.Font(size=35, weight='bold', family='Courier-New')
    label['font'] = label_font

    btn_font = font.Font(size=25)
    button1 = tk.Button(root, text="Train New",bg='lime',fg='black',
                        command=data_collection, height=2, width=20)
    button1.grid(row=1, column=0, pady=(10, 10), padx=(5, 5))
    button1['font'] = btn_font

    button2 = tk.Button(root, text="Identify Known",bg='orange',fg='black',
                        command=facerecognition, height=2, width=20)
    button2.grid(row=1, column=1, pady=(10, 10), padx=(5, 5))
    button2['font'] = btn_font

    button3 = tk.Button(root, text="Exit",
                        command=root.destroy, height=2, width=20, bg='red',fg='black')
    button3.grid(row=2, column=0, pady=(10, 10), padx=(5, 5),columnspan=2)
    button3['font'] = btn_font
    root.mainloop()
    return
