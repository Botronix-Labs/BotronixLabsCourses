import tkinter as tk

def move_forward():
    print("Moving Forward")

def move_back():
    print("Moving Backward")

def move_left():
    print("Turning Left")

def move_right():
    print("Turning Right")

# Create the main window
root = tk.Tk()
root.title("Pico Otto GUI")
root.geometry("300x300")  # Set window size

#Add a title 
title_label = tk.Label(root, text="Pico Otto Direction Control", font=("Arial", 14))
title_label.pack(pady=5)

# Create a labeled frame with fixed size
movement_frame = tk.LabelFrame(root, text="Movement Controls", font=("Arial", 12),
                               borderwidth=2, relief="groove", padx=10, pady=10)
movement_frame.pack(pady=10)



# Create directional buttons
forward_btn = tk.Button(movement_frame, text="↑ Forward")
left_btn = tk.Button(movement_frame, text="← Left")
right_btn = tk.Button(movement_frame, text="→ Right")
back_btn = tk.Button(movement_frame, text="↓ Back")

#Link the buttons to the functions
forward_btn.config(command=move_forward)
back_btn.config(command=move_back)
left_btn.config(command=move_left)
right_btn.config(command=move_right)


# Place them in a grid like a game controller
forward_btn.grid(row=0, column=1)
left_btn.grid(row=1, column=0)
right_btn.grid(row=1, column=2)
back_btn.grid(row=2, column=1)

root.mainloop()




