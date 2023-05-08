# importing of all necessary libraries and packages and functions from different files
# tkinter for gui elements manipulation
import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
from recording import record
from livefeedtest import live
from motiondetection import motiondetect
from designate import designate
from findmotiontheft import find_motion
from inoutdetection import in_out_detection


class Surveillance:
    # tkinter for gui element

    # window creation
    window = tk.Tk()
    # setting window title
    window.title("Smart Home Surveillance Application")
    # setting top menu icon for the window
    window.iconphoto(False, tk.PhotoImage(file='icons/smart-house.png'))

    # setting resolution of the window or the window metrics
    window.geometry('1400x700')

    window.minsize(1400, 700)
    window.maxsize(1400, 700)

    # the frame bound within the window
    frame1 = tk.Frame(window)

    label_title = tk.Label(frame1, text="Smart Home Surveillance Application")
    label_font = font.Font(size=30, weight='bold', family='Courier New')
    label_title['font'] = label_font
    label_title.grid(pady=(10, 10), column=2)

    # main hero image of the application icon setting
    icon = Image.open('icons/smart-house.png')
    icon = icon.resize((150, 150), Image.Resampling.LANCZOS)
    icon = ImageTk.PhotoImage(icon)
    label_icon = tk.Label(frame1, image=icon)
    label_icon.grid(row=1, pady=(5, 10), column=2)

    # icon dimension manipulation for different buttons made available
    btn1_image = Image.open('icons/webcam.png')
    btn1_image = btn1_image.resize((40, 40), Image.Resampling.LANCZOS)
    btn1_image = ImageTk.PhotoImage(btn1_image)
    #designate button designing element
    btn2_image = Image.open('icons/designate.png')
    btn2_image = btn2_image.resize((40, 40), Image.Resampling.LANCZOS)
    btn2_image = ImageTk.PhotoImage(btn2_image)
    #exit button designing element
    btn5_image = Image.open('icons/exit.png')
    btn5_image = btn5_image.resize((40, 40), Image.Resampling.LANCZOS)
    btn5_image = ImageTk.PhotoImage(btn5_image)
    #motion detection design element
    btn3_image = Image.open('icons/motion-sensor.png')
    btn3_image = btn3_image.resize((40, 40), Image.Resampling.LANCZOS)
    btn3_image = ImageTk.PhotoImage(btn3_image)
    #in out detection design element
    btn6_image = Image.open('icons/walk.png')
    btn6_image = btn6_image.resize((40, 40), Image.Resampling.LANCZOS)
    btn6_image = ImageTk.PhotoImage(btn6_image)
    #recording button design element
    btn4_image = Image.open('icons/recording.png')
    btn4_image = btn4_image.resize((40, 40), Image.Resampling.LANCZOS)
    btn4_image = ImageTk.PhotoImage(btn4_image)
    #facial recognition or identification functionality button design element
    btn7_image = Image.open('icons/face-recognition.png')
    btn7_image = btn7_image.resize((40, 40), Image.Resampling.LANCZOS)
    btn7_image = ImageTk.PhotoImage(btn7_image)

    # --------------- Button Functionalities, text rendering and alignments -------------------#
    btn_font = font.Font(size=20)
    btn1 = tk.Button(frame1, text='Monitor', height=90, width=200, fg='black', bg='aqua', image=btn1_image,
                     compound='left', command=find_motion)
    btn1['font'] = btn_font
    btn1.grid(row=3, pady=(20, 10))

    #for designated area motion detection functionality 
    btn2 = tk.Button(frame1, text='Designation', height=90, width=200, fg='black', bg='lime', compound='left', command=designate,
                     image=btn2_image)
    btn2['font'] = btn_font
    btn2.grid(row=3, pady=(20, 10), column=3)

    #for motion detection functionality
    btn_font = font.Font(size=22)
    btn3 = tk.Button(frame1, text='Motion', height=90, width=200, fg='black', bg='lime', image=btn3_image,
                     compound='left', command=motiondetect)
    btn3['font'] = btn_font
    btn3.grid(row=5, pady=(20, 10))
    #for recording footage functionality
    btn4 = tk.Button(frame1, text='Recording', height=90, width=200, fg='black', bg='lime', image=btn4_image,
                     compound='left', command=record)
    btn4['font'] = btn_font
    btn4.grid(row=5, pady=(20, 10), column=3)
    #in out detection functionality
    btn6 = tk.Button(frame1, text='In-Out', height=90, width=200, fg='black', bg='lime', image=btn6_image,
                     compound='left',command=in_out_detection)
    btn6['font'] = btn_font
    btn6.grid(row=5, pady=(20, 10), column=2)
    #exit button functionality to exit the program on click
    btn5 = tk.Button(frame1, text='Exit', height=90, width=200,
                     fg='black', bg='lightblue', image=btn5_image, compound='left', command=window.destroy)
    btn5['font'] = btn_font
    btn5.grid(row=6, pady=(20, 10), column=2)

    btn7 = tk.Button(frame1, text="Identify", fg="black", bg='yellow', compound='left', image=btn7_image, height=90,
                     width=200)
    btn7['font'] = btn_font
    btn7.grid(row=3, column=2, pady=(20, 10))

    # frame packing and fixing the window
    frame1.pack()
    window.mainloop()
