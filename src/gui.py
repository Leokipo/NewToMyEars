import tkinter as tk
def displayGenreSelection():
    root = tk.Tk()
    root.geometry("700x700")
    root.title("NewToMyEars")

    tk.Label(root, text="Welcome to NewToMyEars!", font=("Arial", 20)).pack(padx=10, pady=10)
    tk.Label(root, text="Type a genre to make a playlist of new music", font=("Arial", 16)).pack(padx=10, pady=10)

    # retrieve genre input from Entry field
    genre = tk.StringVar()
    tk.Entry(root, textvariable=genre, font=("Arial", 16)).pack(padx=10, pady=10)

    root.mainloop()

displayGenreSelection()