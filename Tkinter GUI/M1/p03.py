import tkinter as tk

def greet(): #defines a Python function.
    label.config(text="Hello, Robot Builder!") # changes the label text dynamically.

root = tk.Tk()
root.title("Robot Greeter")
root.geometry("300x200")

label = tk.Label(root, text="Welcome!", font=("Arial", 14))
label.pack(pady=10)

button = tk.Button(root, text="Greet", command=greet) #binds the button to the function.
button.pack()

root.mainloop()
