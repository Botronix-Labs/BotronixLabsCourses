import tkinter as tk

def show_name():
    name = entry.get() #.get() retrieves the text from the Entry.
    label.config(text=f"Hello, {name}!") #You can use f-strings to format dynamic messages.

root = tk.Tk()
root.title("Name Greeter")
root.geometry("300x200")

entry = tk.Entry(root, font=("Arial", 12)) #Entry is a text box for user input.
entry.pack(pady=10)

button = tk.Button(root, text="Say Hello", command=show_name)
button.pack()

label = tk.Label(root, text="", font=("Arial", 14))
label.pack(pady=10)

root.mainloop()
