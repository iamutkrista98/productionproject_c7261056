# importing of necessary libraries
from tkinter import *
from tkinter import messagebox
import subprocess
import sqlite3

# creating a connection to database
conn = sqlite3.connect('authentication.db')
cursor = conn.cursor()

# create a table for storing the credentials (if it doesn't exist)
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,Name TEXT,username TEXT, password TEXT)''')
conn.commit()

root = Tk()
root.title('Login')
root.geometry('925x500+300+200')

root.attributes('-alpha', 0.95)
# getting the current screen resolution
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# evaluating the center position
xpos = (screen_width/2)-(925/2)
ypos = (screen_height/2)-(500/2)
root.geometry("+%d+%d" % (xpos, ypos))
root.configure(bg='#fff')
root.resizable(False, False)


def sign_up():
    app_path = 'signup.py'
    subprocess.Popen(['python', app_path])
    root.destroy()


def login():
    username = user.get()
    password = code.get()

    # query the database to check if the credentials are valid
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Authentication Successful",
                            "Redirecting to Application!")
        app_path = 'mainhub.py'
        subprocess.Popen(['python', app_path])
        root.destroy()

    else:
        messagebox.showerror("Authentication Error!",
                             "Invalid Username or Password Supplied!")


img = PhotoImage(file='icons/intro.png')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)

heading = Label(frame, text='Login', fg='#57a1f8', bg='white',
                font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# -----------------------


def on_enter(e):
    user.delete(0, 'end')


def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')


user = Entry(frame, width=25, fg='black', border=0,
             bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')

user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)
# ------------------------------------------------------


def on_enter(e):
    code.delete(0, 'end')


def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')


code = Entry(frame, width=25, fg='black', border=0,
             bg='white', font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# --------
Button(frame, width=39, pady=7, text='Login', bg='#57a1f8',
       fg='white', border=0, command=login).place(x=35, y=204)
label = Label(frame, text='Dont Have Credentials? ', fg='black',
              bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

sign_up = Button(frame, width=6, text='Sign Up', border=0,
                 bg='white', cursor='hand2', fg='#57a1f8', command=sign_up)
sign_up.place(x=215, y=270)


root.mainloop()

conn.close()
