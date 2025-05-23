import tkinter as tk

# Create the main window for the GUI
root = tk.Tk()
root.title("Pico Otto Robot Control")
root.geometry("500x400")  # Adjusted to fit all buttons and image nicely
root.configure(bg="#e6f2ff")  # Light background for a clean look

# Add a main title label at the top
title = tk.Label(
    root, text="Robot Controller",
    font=("Arial", 18, "bold"),
    fg="blue", bg="lightgray"
)
title.pack(pady=10)

# Load the robot image (ensure the image exists at this location)
robot_img = tk.PhotoImage(file=r"C:\Users\tonyc\Downloads\robot.png")

# Display the robot image
img_label = tk.Label(root, image=robot_img, bg="lightgray")
img_label.pack()

# Create a frame for movement control buttons
frame = tk.LabelFrame(
    root, text="Movement",
    font=("Arial", 12, "bold"),
    padx=10, pady=10,
    bg="white"
)
frame.pack(pady=15)

# Create control buttons
# Arrange buttons in a D-pad layout
btn_forward = tk.Button(frame, text="Forward", width=12, bg="green", fg="white")
btn_forward.grid(row=0, column=1, pady=5)

btn_left = tk.Button(frame, text="Left", width=12, bg="orange")
btn_left.grid(row=1, column=0, padx=5)

btn_right = tk.Button(frame, text="Right", width=12, bg="orange")
btn_right.grid(row=1, column=2, padx=5)

btn_backward = tk.Button(frame, text="Backward", width=12, bg="red", fg="white")
btn_backward.grid(row=2, column=1, pady=5)

# Start the Tkinter main loop
root.mainloop()

