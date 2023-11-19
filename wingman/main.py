import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import collections
import matplotlib.pyplot as plt

class PieChart:
    def __init__(self, categories_count):
        self.categories_count = categories_count

    def generate_chart(self):
        if self.categories_count:
            categories = list(self.categories_count.keys())
            counts = list(self.categories_count.values())

            plt.figure(figsize=(8, 6))
            plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title('Category Distribution - Pie Chart')
            plt.show()
        else:
            messagebox.showwarning("Warning", "No data to generate a pie chart!")


class BarGraph:
    def __init__(self, categories_count):
        self.categories_count = categories_count

    def generate_chart(self):
        if self.categories_count:
            categories = list(self.categories_count.keys())
            counts = list(self.categories_count.values())

            colors = plt.cm.tab20c.colors[:len(categories)]

            plt.figure(figsize=(10, 6))
            bars = plt.bar(categories, counts, color=colors)
            plt.xlabel('Categories')
            plt.ylabel('Counts')
            plt.title('Category Distribution - Bar Graph')
            plt.xticks(rotation=45)

            plt.legend(bars, categories)

            plt.tight_layout()
            plt.show()
        else:
            messagebox.showwarning("Warning", "No data to generate a bar graph!")


class Task:
    def __init__(self, name, status="Pending", due_date=None, priority="Medium", category=None):
        self.name = name
        self.status = status
        self.due_date = due_date
        self.priority = priority
        self.category = category

class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wingman - Your friend")
        self.configure(bg="#D4F1F4")
        self.geometry("")

        self.title_font = ('DIN', 50)
        self.main_font = ('Bell MT', 12)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # First Tab - Tasks
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Tasks')

        tk.Label(self.tab1, text="Wingman", font=self.title_font, bg="#B1D4E0").pack(
            expand=True, fill="both", padx=10, pady=5)

        self.list_box = tk.Listbox(self.tab1, font=self.main_font, bg="#FFFFFF", fg="#000000", relief='sunken')
        self.list_box.pack(expand=True, fill="both", padx=10, pady=5)

        self.entry_box = tk.Entry(self.tab1, font=self.main_font, bg="#FFFFFF", fg="#000000", relief='sunken')
        self.entry_box.pack(expand=True, fill="both", padx=10, pady=5)

        label_frame = tk.LabelFrame(self.tab1, text="Options", font=self.main_font, bg="#D4F1F4")
        label_frame.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.add_button = tk.Button(label_frame, text="Add Task", font=self.main_font, command=self.add_task)
        self.add_button.pack(expand=True, fill="both", padx=10, pady=5)

        self.delete_button = tk.Button(label_frame, text="Delete Task", font=self.main_font, command=self.delete_task)
        self.delete_button.pack(expand=True, fill="both", padx=10, pady=5)

        self.import_button = tk.Button(label_frame, text="Import Text File", font=self.main_font, command=self.import_task)
        self.import_button.pack(expand=True, fill="both", padx=10, pady=5)

        self.view_button = tk.Button(label_frame, text="View File Details", font=self.main_font, command=self.view_details)
        self.view_button.pack(expand=True, fill="both", padx=10, pady=5)

        # Second Tab - Status Tab
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Category')

        # Treeview for displaying tasks in Status tab
        self.tree_view = ttk.Treeview(self.tab2, columns=("Tasks", "Category"), show="headings")
        self.tree_view.heading("Tasks", text="Tasks")
        self.tree_view.heading("Category", text="Category")
        self.tree_view.pack(expand=True, fill="both", padx=10, pady=5)

        # Third Tab - Distribution
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Distribution')

        label_frame_distribution = tk.LabelFrame(self.tab3, text="Chart Type", font=self.main_font, bg="#D4F1F4")
        label_frame_distribution.pack(expand=True, fill="both", padx=10, pady=5)

        self.chart_type_var = tk.StringVar(self.tab3)
        self.chart_type_var.set("Select Chart Type")  # Default selection
        chart_options = ["Pie Chart", "Bar Graph"]
        self.chart_dropdown = ttk.Combobox(label_frame_distribution, textvariable=self.chart_type_var, values=chart_options, state="readonly")
        self.chart_dropdown.pack(expand=True, fill="both", padx=10, pady=5)

        self.chart_button = tk.Button(self.tab3, text="Generate Chart", font=self.main_font, command=self.generate_chart)
        self.chart_button.pack(expand=True, fill="both", padx=10, pady=5)

        

class Main(BaseApp):
    def __init__(self):
        super().__init__()
        self.load_tasks()

    def refresh_tree_view(self):
        # Clear existing items in the tree view
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
        
        # Reload tasks to update the tree view
        self.load_tasks()

    def delete_task(self):
        selected_task_index = self.list_box.curselection()
        if selected_task_index:
            selected_task = self.list_box.get(selected_task_index)
            confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete {selected_task}?")
            if confirmation:
                try:
                    category = self.get_category(selected_task)
                    file_name = f"{selected_task}_{category}.txt" if category else f"{selected_task}.txt"
                    os.remove(file_name)
                    self.list_box.delete(selected_task_index)
                    messagebox.showinfo("Success", f"{selected_task} has been deleted!")
                    self.refresh_tree_view()  # Refresh the tree view after deletion
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete {selected_task}: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select a task to delete!")

    def add_task(self):
        task_name = self.entry_box.get().strip()
        if not task_name:
            messagebox.showwarning("Warning", "Task name cannot be empty or contain only spaces!")
            return

        category = simpledialog.askstring("Category", "Enter task category:")
        if category is None:  # Check if the user clicked 'Cancel'
            return

        if not category.strip():  # Check if the category is empty or contains only spaces
            messagebox.showwarning("Warning", "Category name cannot be empty or contain only spaces!")
            return

        try:
            task = Task(name=task_name, category=category)
            self.list_box.insert(tk.END, task.name)
            self.entry_box.delete(0, tk.END)
            self.save_to_file(task)
            messagebox.showinfo("Success", f"{task.name} has been created!")
            self.refresh_tree_view()  # Refresh the tree view after addition
        except ValueError as e:
            messagebox.showerror("Error", str(e))


    def save_to_file(self, task):
        try:
            file_name = f"{task.name}_{task.category}.txt" if task.category else f"{task.name}.txt"
            with open(file_name, "w") as file:
                file.write(task.name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def load_tasks(self):
        # Clear the existing list box and tree view items before loading tasks
        self.list_box.delete(0, tk.END)
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        # Load tasks
        for file_name in os.listdir():
            if file_name.endswith(".txt"):
                task_name, category = os.path.splitext(file_name)[0].split('_') if '_' in file_name else (os.path.splitext(file_name)[0], None)
                task = Task(name=task_name, category=category)
                self.list_box.insert(tk.END, task.name)
                self.tree_view.insert("", "end", values=(task.name, task.category))

    def get_category(self, task_name):
        for file_name in os.listdir():
            if file_name.startswith(f"{task_name}_") and file_name.endswith(".txt"):
                return file_name[len(task_name) + 1:-4]  # Extract the category
        return None

    def import_task(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if file_path:
            file_name = os.path.basename(file_path)
            task_name = os.path.splitext(file_name)[0]
            category = simpledialog.askstring("Category", f"Enter category for '{task_name}':")

            try:
                destination = f"{task_name}_{category}.txt" if category else f"{task_name}.txt"
                with open(file_path, "r") as source_file:
                    content = source_file.read()

                with open(destination, "w") as dest_file:
                    dest_file.write(content)

                self.list_box.insert(tk.END, task_name)
                messagebox.showinfo("Success", f"{task_name} has been imported!")
                self.refresh_tree_view()  # Refresh the tree view after import
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import {file_name}: {str(e)}")


    def view_details(self):
        selected_task_index = self.list_box.curselection()
        if selected_task_index:
            selected_task = self.list_box.get(selected_task_index)
            category = self.get_category(selected_task)  # Get the category for the selected task
            file_name = f"{selected_task}_{category}.txt" if category else f"{selected_task}.txt"  # Form the correct file name

            details_window = tk.Toplevel(self)
            details_window.title(f"Details of {selected_task}")
            details_window.geometry("1000x800")

            details_label = tk.Label(details_window, text=f"Details of {selected_task}", font=self.main_font)
            details_label.pack(padx=10, pady=5)

            content_label = tk.Label(details_window, text="Content:", font=self.main_font)
            content_label.pack(padx=10, pady=5)

            text_area = tk.Text(details_window, font=self.main_font, bg="#FFFFFF", fg="#000000", relief='sunken')
            text_area.pack(expand=True, fill="both", padx=10, pady=5, anchor='n')

            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    content = file.read()
                    text_area.insert(tk.END, content)

            def save_content():
                content = text_area.get("1.0", tk.END)
                with open(file_name, "w") as file:
                    file.write(content)
                messagebox.showinfo("Saved", "The content has been saved!")

            save_button = tk.Button(details_window, text="Save Content", font=self.main_font,
                                    command=save_content)
            save_button.pack(padx=10, pady=5, anchor='s')
        else:
            messagebox.showwarning("Warning", "Please select a task to view details!")

    def generate_chart(self):
        selected_chart = self.chart_type_var.get()
        categories_count = self.get_categories_count()

        chart = None
        if selected_chart == "Pie Chart":
            chart = PieChart(categories_count)
        elif selected_chart == "Bar Graph":
            chart = BarGraph(categories_count)

        if chart:
            chart.generate_chart()
        else:
            messagebox.showwarning("Warning", "Please select a chart type!")

    def get_categories_count(self):
        categories_count = collections.defaultdict(int)
        for file_name in os.listdir():
            if file_name.endswith(".txt"):
                task_name, category = os.path.splitext(file_name)[0].split('_') if '_' in file_name else (os.path.splitext(file_name)[0], None)
                categories_count[category] += 1
        return categories_count

if __name__ == "__main__":
    app = Main()
    app.mainloop()
