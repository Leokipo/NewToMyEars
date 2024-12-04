import tkinter as tk
import webbrowser

def displayUserAuth(authorization_url):
    root = tk.Tk()
    root.geometry("700x700")
    root.title("Spotify Authentication")
    webbrowser.open(authorization_url)

def displayGenreSelection():
    root = tk.Tk()
    root.geometry("700x700")
    root.title("NewToMyEars")

    tk.Label(root, text="Welcome to NewToMyEars!", font=("Arial", 20)).pack(padx=10, pady=10)
    tk.Label(root, text="Type a genre to make a playlist of new music", font=("Arial", 16)).pack(padx=10, pady=10)

    # retrieve genre input from Entry field
    genreVar = tk.StringVar()
    tk.Entry(root, textvariable=genreVar, font=("Arial", 16)).pack(padx=10, pady=10)

    def getGenre():
        genre = genreVar.get().lower()
        print(genre)

    tk.Button(root, text="Generate Playlist", command=getGenre).pack(padx=10, pady=10)

    root.mainloop()

# displayGenreSelection()