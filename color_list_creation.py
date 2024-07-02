import tkinter as tk
from tkinter import ttk, messagebox
from tkcolorpicker import askcolor

class ColorListCreationWindow(tk.Toplevel):
    def __init__(self, parent, db_conn):
        super().__init__(parent)
        self.title("Create Color List")
        self.geometry("400x300")  # Set a default size for the window
        self.db_conn = db_conn
        self.create_widgets()
        self.load_colors()

    def create_widgets(self):
        # Color Name Entry
        ttk.Label(self, text="Color Name:").grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.color_name_entry = ttk.Entry(self)
        self.color_name_entry.grid(column=1, row=0, padx=10, pady=5, sticky='w')

        # Color Picker Button
        self.color_button = ttk.Button(self, text="Select Color", command=self.select_color)
        self.color_button.grid(column=0, row=1, padx=10, pady=5, sticky='w')

        # Color Display
        self.color_display = tk.Canvas(self, width=50, height=25, bg="white", bd=2, relief="sunken")
        self.color_display.grid(column=1, row=1, padx=10, pady=5, sticky='w')

        # Save Button
        self.save_button = ttk.Button(self, text="Save Color", command=self.save_color)
        self.save_button.grid(column=0, row=2, columnspan=2, padx=10, pady=10, sticky='ew')

        # Color List Display
        self.color_listbox = tk.Listbox(self, height=10)
        self.color_listbox.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky='nsew')

    def select_color(self):
        color = askcolor()[1]
        if color:
            self.selected_color = color
            self.color_display.config(bg=color)

    def save_color(self):
        color_name = self.color_name_entry.get()
        if not color_name or not hasattr(self, 'selected_color'):
            messagebox.showerror("Error", "Please enter a color name and select a color.")
            return

        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO colors (name, hex_value)
            VALUES (?, ?)
        ''', (color_name, self.selected_color))
        self.db_conn.commit()

        self.color_name_entry.delete(0, tk.END)
        self.color_display.config(bg="white")
        self.load_colors()

    def load_colors(self):
        self.color_listbox.delete(0, tk.END)

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT name, hex_value FROM colors")
        colors = cursor.fetchall()

        for color in colors:
            self.color_listbox.insert(tk.END, f"{color[0]}: {color[1]}")

