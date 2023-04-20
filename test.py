import tkinter as tk


window = tk.Tk()

greeting = tk.Label(text="hello,world!")

greeting.pack()

label = tk.Label(
    text="Hello, Tkinter",
    foreground="white",  # Set the text color to white
    background="black"  # Set the background color to black
)
label.pack()

button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)
button.pack()

entry = tk.Entry(fg="yellow", bg="blue", width=50)
label1 = tk.Label(text="Name")
entry=tk.Entry()

label1.pack()
entry.pack()

window.mainloop()