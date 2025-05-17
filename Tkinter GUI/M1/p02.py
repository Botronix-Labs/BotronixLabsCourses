import tkinter as tk

root = tk.Tk()
root.title("Label and Button")
root.geometry("300x200")

# Add a Label
label = tk.Label(root, text="Welcome to Robotics!", font=("Arial", 14)) #displays text.
label.pack(pady=10) #automatically places the widgets vertically. adds vertical spacing.

# Add a Button
button = tk.Button(root, text="Click Me") #creates a clickable button.
button.pack()

root.mainloop()
