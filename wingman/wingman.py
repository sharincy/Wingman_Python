import tkinter as tk
from tkinter import messagebox, filedialog
import os

class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wingman - Your friend")
        self.configure(bg="#D4F1F4")
        self.geometry("")

        self.head_font = ('DIN', 50)
        self.body_font = ('Bell MT', 12)

        tk.Label(self, text="Wingman", font=self.head_font,
                 bg="#B1D4E0").pack(expand=True, fill="both", padx=10, pady=5)

        self.list_box = tk.Listbox(self, font=self.body_font, bg="#FFFFFF", fg="#000000", relief='sunken')
        self.list_box.pack(expand=True, fill="both", padx=10, pady=5)

        self.entry_box = tk.Entry(self, font=self.body_font, bg="#FFFFFF", fg="#000000", relief='sunken')
        self.entry_box.pack(expand=True, fill="both", padx=10, pady=5)

        label_frame = tk.LabelFrame(self, text="Options", font=self.body_font, bg="#D4F1F4")
        label_frame.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.add_button = tk.Button(label_frame, text="Add Task", font=self.body_font, 
                                command=self.add_task)
        self.add_button.pack(expand=True, fill="both", padx=10, pady=5)

        self.view_button = tk.Button(label_frame, text="View File Details", font=self.body_font,
                                command=self.view_details)
        self.view_button.pack(expand=True, fill="both", padx=10, pady=5)

    def add_task(self):
        pass

    def save_to_file(self, task):
        pass

    def load_tasks(self):
        pass

    def view_details(self):
        pass

class App(BaseApp):
    def __init__(self):
        super().__init__()
        self.load_tasks()

    def add_task(self):
        task = self.entry_box.get()
        try:
            if not task.strip():  # Check if the task contains only whitespace characters
                raise ValueError("Task name cannot be empty or contain only spaces!")
            
            self.list_box.insert(tk.END, task)
            self.entry_box.delete(0, tk.END)
            self.save_to_file(task)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def save_to_file(self, task):
        try:
            file_name = f"{task}.txt"
            with open(file_name, "w") as file:
                file.write(task)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def save_to_file(self, task):
        file_name = f"{task}.txt"
        with open(file_name, "w") as file:
            file.write(task)

    def load_tasks(self):
        for file_name in os.listdir():
            if file_name.endswith(".txt"):
                task = os.path.splitext(file_name)[0]
                self.list_box.insert(tk.END, task)

    def view_details(self):
        selected_task = self.list_box.get(tk.ACTIVE)
        if selected_task:
            details_window = tk.Toplevel(self)
            details_window.title(f"Details of {selected_task}")
            details_window.geometry("1000x800")  # Set a fixed size for the window

            details_label = tk.Label(details_window, text=f"Details of {selected_task}", font=self.body_font)
            details_label.pack(padx=10, pady=5)

            content_label = tk.Label(details_window, text="Content:", font=self.body_font)
            content_label.pack(padx=10, pady=5)

            text_area = tk.Text(details_window, font=self.body_font, bg="#FFFFFF", fg="#000000", relief='sunken')
            text_area.pack(expand=True, fill="both", padx=10, pady=5, anchor='n')  # Anchor text area to the top

            file_name = f"{selected_task}.txt"
            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    content = file.read()
                    text_area.insert(tk.END, content)

            def save_content():
                content = text_area.get("1.0", tk.END)
                with open(file_name, "w") as file:
                    file.write(content)

            save_button = tk.Button(details_window, text="Save Content", font=self.body_font,
                                    command=save_content)
            save_button.pack(padx=10, pady=5, anchor='s')  # Anchor button to the bottom

if __name__ == "__main__":
    app = App()
    app.mainloop()
