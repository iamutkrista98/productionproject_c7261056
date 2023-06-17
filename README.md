# productionproject_c7261056
Product Guidelines
The product in its entirety was coded in Python programming language. For the GUI interface tkinter library was utilized with properly planned design approach and well-established use cases. 
Login and Sign Up:
 
Screenshot: Application Login Page
If the user is signing up for first time one must press the signup link on the bottom to open up the signup window, validation has also been kept in check in order to not allow user to register with same user name against the database
 
Screenshot: Signup Process Validation against unique username

After supplying new username information, the user is successfully registered, and is able to login with the new credentials and they will be redirected to login page as well. Since this is a portable application with local database implementation, no further verification is required. 
 
Screenshot: Successful Signup process

 
Screenshot: Logging using the new credentials


 
Screenshot: Successful Login and Redirection
 
Screenshot: Application GUI Interface greeted after successful login
The application interface provides its different functionalities laid out in the form of buttons that corresponds to different application relevant to home surveillance related functionalities in the form of buttons with respective iconographies and transluscent design. 
Recording Functionality:
Beginning with the record functionality. The record functionality as its name functions by recording the live frames captured with a timestamp and saves to disk. The app has been built in such a way that it is capable of recognizing the native resolution of the camera interfaced with it. For the particular demonstration, camera from a phone has been interfaced to the computer. Just by clicking on the record button, the recording is started which has been depicted below: To exit out of the recording mode esc key has to be pressed. 
 
Screenshot: Recording Functionality Initialized
The recording is saved into the footages folder within the program folder with proper timestamp. The writing of video has been optimized in such a way that it saves the video in mp4 format so that it is universally compatible.
If higher resolution camera or even ip camera is interfaced into the system running the application it is capable of recording the footage in its native resolution and the size of the video varies accordingly.
 
Screenshot: Recording Functionality Successfully Saved Footages
Motion Detection Functionality:
The next intuitive functionality provided within the application in motion detection. The functionality works by comparing the two consecutive frames captured in realtime and evaluating the differences after thresholding i.e noise removal it identifies whether motion has occurred or not. This mode in particular is capable of detecting even small movement and draws a boundary over the section where motion occurred with proper notation.
 
Screenshot: Motion Detection Functionality, no motion 
 
Screenshot: Motion Detection Functionality, motion detected with boundary added

Designated Area Motion Detection Functionality:
The next feature integration to the application is designate whereby one can select the area using the right and left click mouse button to set an area bounding diagonally such that motion detection will only be carried out over at that designated area. This functionality in particular is integrated with push notification and send in push notification at regular intervals if motion by chance occurred in the bounded region. This functionality can really come in handy in the case where one has a safe in their room, and by bounding the area covered by the safe within the room the one that is monitoring could keep a piece of mind by regularly receiving notification alert when motion occurred in that region so that they can become alert at those times and perform actions necessary. If by any chance notification delivery fails, the delivery status and the appropriate alert are stored over at the local machine within the notificationlog for later reference with proper timestamp and detailing. 
  
Screenshot: Designated Motion Initial Opening to select area
 
Screenshot: Designated Area Selected, Currently no motion occurred
 
Screenshot: Motion Occurrence in designated area
 
Screenshot: Notification Delivered to the Mobile Device 20s interval
 
Screenshot: Notification Log Maintained accordingly with timestamp
Visitor In and Out Detection Functionality:
The other functionality provided within the application is visitor in and out. This functionality works based on motion detection with mathematical evaluation of the direction where motion occurred. The visitor that moves towards the left axis is evaluated to be in and the one that is moving to right is evaluated to have gone out. The functionality is provided with the ability to capture regular snapshots of during the entry and exit out of the frame by visitors and save those snaps on folders within the project directory inside visitors and its subfolders in and out respectively.
 
 
 
 
Screenshot: Visitors In images on the in directory
 
Screenshot: Visitors Out within the Out Directory
Face Identification and Training Functionality:
The next functionality integrated into the application is Identification. On Clicking the identify button, one is greeted with another interface 
 
Screenshot: Identify Functionality Options Window
 
Screenshot: Train New Options, Provide Details
 
Screenshot: Train New Options, Provided Details

 
Screenshot: Starting to capture images samples of the face, 100 samples captured
 
 
Screenshot: Grayscale face image samples saved to disk, and a trainingmodel.yml created with vector mapping
 
Screenshot: Successfully identified the face data that was trained on appearance in identify known option 
 
Screenshot: Successfully identified the unknown face data with proper mapping that has not been trained 
 

 
Screenshot: After Successful training and identifying against new image of same person
 
Screenshot: Training model yml updated in disk with proper labelling
The above functionality is also integrated with timed notification delivery for any unknown person identified within the frame to send alert. 
 
Screenshot: Push notification for unknown visitor in frame
 
Screenshot: Notification Log for above case
Monitoring Functionality
The next functionality integrated into the application is Monitoring. This needs a really isolated environment whereby it takes time to capture the frame of the surrounding prior to next stepping. It then compares the frame that was captured in a still environment against the frame catured after any movement. Based on structural similarity it generates a score evaluating the rate of difference between the two frames. This indicates possible suspected theft.  

 
Screenshot: Similarity Score Calculation and differential frame marked
 
Screenshot: Differential frame parts marked and saved to disk
