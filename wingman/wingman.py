import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
from datetime import datetime

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Todo App")
        self.window.configure(bg="#F7F7F5")
        self.window.geometry("400x150")

        self.head_font = ('Leelawadee UI', 20)
        self.body_font = ('Leelawadee UI', 12)

        tk.Label(self.window, text="Todo App", font=self.head_font,
                 bg="#F0E68C").pack(expand=True, fill="both", padx=10, pady=5)
        
        # Create PhotoImage after the root window is initialized
        self.photo = tk.PhotoImage(file='D:\Programming_Files\picture\S__22822914.png')
        self.photo2 = tk.PhotoImage(file='S__22822914.png')

        new_button = tk.Button(self.window, text="New File", font=self.body_font, bg='#4CAF50', fg='#FFFFFF',
                               activebackground='#3E8E41', relief='groove', command=self.new, image=self.photo, compound= 'bottom')
        new_button.pack(expand=True, fill="both", padx=10, pady=5)
        open_button = tk.Button(self.window, text="Open File", font=self.body_font, bg='#FA8072', fg='#FFFFFF',
                                activebackground='#DD4124', relief='groove', command=self.open, image=self.photo2, compound= 'bottom')
        open_button.pack(expand=True, fill="both", padx=10, pady=5)

        self.window.mainloop()

    def new(self):
        pass

    def open(self):
        pass

if __name__ == "__main__":
    app = App()
