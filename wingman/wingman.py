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

        self.delete_button = tk.Button(label_frame, text="Delete Task", font=self.body_font,
                                command=self.delete_task)
        self.delete_button.pack(expand=True, fill="both", padx=10, pady=5)

        self.view_button = tk.Button(label_frame, text="View File Details", font=self.body_font,
                                command=self.view_details)
        self.view_button.pack(expand=True, fill="both", padx=10, pady=5)

        self.import_button = tk.Button(label_frame, text="Import Text File", font=self.body_font,
                                command=self.import_task)
        self.import_button.pack(expand=True, fill="both", padx=10, pady=5)

    def add_task(self):
        pass

    def save_to_file(self, task):
        pass

    def load_tasks(self):   
        pass

    def view_details(self):
        pass

class Main(BaseApp):
    def __init__(self):
        super().__init__()
        self.load_tasks()

    def delete_task(self):
        selected_task_index = self.list_box.curselection()
        if selected_task_index:
            selected_task = self.list_box.get(selected_task_index)
            confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete {selected_task}?")
            if confirmation:
                try:
                    file_name = f"{selected_task}.txt"
                    os.remove(file_name)
                    self.list_box.delete(selected_task_index)
                    messagebox.showinfo("Success", f"{selected_task} has been deleted!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete {selected_task}: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select a task to delete!")

    def add_task(self):
        task = self.entry_box.get()
        try:
            if not task.strip():
                raise ValueError("Task name cannot be empty or contain only spaces!")
            
            self.list_box.insert(tk.END, task)
            self.entry_box.delete(0, tk.END)
            self.save_to_file(task)
            messagebox.showinfo("Success", f"{task} has been created!")
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

    def import_task(self):
        # Prompt the user to select a file
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if file_path:
            # Extract the file name
            file_name = os.path.basename(file_path)
            task_name = os.path.splitext(file_name)[0]

            try:
                # Copy the file to your application's folder
                destination = f"{task_name}.txt"
                with open(file_path, "r") as source_file, open(destination, "w") as dest_file:
                    content = source_file.read()
                    dest_file.write(content)

                # Update the list box to display the newly imported task
                self.list_box.insert(tk.END, task_name)
                messagebox.showinfo("Success", f"{task_name} has been imported!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import {file_name}: {str(e)}")

    def view_details(self):
        selected_task_index = self.list_box.curselection()
        if selected_task_index:
            selected_task = self.list_box.get(selected_task_index)
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
                messagebox.showinfo("Saved", "The content has been saved!")

            save_button = tk.Button(details_window, text="Save Content", font=self.body_font,
                                    command=save_content)
            save_button.pack(padx=10, pady=5, anchor='s')  # Anchor button to the bottom
        else:
            messagebox.showwarning("Warning", "Please select a task to view details!")

if __name__ == "__main__":
    app = Main()
    app.mainloop()
