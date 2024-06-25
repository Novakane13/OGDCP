import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import sqlite3
import uuid

class DetailedTicketCreationWindow(tk.Toplevel):
    def __init__(self, parent, db_conn, customer_id, ticket_type_id):
        super().__init__(parent)
        self.parent = parent
        self.db_conn = db_conn
        self.customer_id = customer_id
        self.ticket_type_id = ticket_type_id
        self.title("Create Detailed Ticket")
        self.geometry("1200x800")
        self.create_widgets()
        self.load_ticket_type_details()

    def create_widgets(self):
        # Drop and Due Dates
        ttk.Label(self, text="Drop:").grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.drop_date = DateEntry(self)
        self.drop_date.grid(column=1, row=0, padx=10, pady=5, sticky='w')

        ttk.Label(self, text="Due:").grid(column=2, row=0, padx=10, pady=5, sticky='w')
        self.due_date = DateEntry(self)
        self.due_date.grid(column=3, row=0, padx=10, pady=5, sticky='w')

        # Garments Section
        self.garment_frame = ttk.LabelFrame(self, text="Garments")
        self.garment_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky='ew')

        self.garment_listbox = tk.Listbox(self.garment_frame, height=10)
        self.garment_listbox.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

        # Upcharges Section
        self.upcharge_frame = ttk.LabelFrame(self, text="Upcharges")
        self.upcharge_frame.grid(column=2, row=1, padx=10, pady=10, sticky='ew')

        self.upcharge_vars = {}
        self.upcharge_listbox = tk.Listbox(self.upcharge_frame, height=10)
        self.upcharge_listbox.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

        # Colors and Patterns Section
        self.color_pattern_frame = ttk.LabelFrame(self, text="Colors and Patterns")
        self.color_pattern_frame.grid(column=3, row=1, padx=10, pady=10, sticky='ew')

        self.color_listbox = tk.Listbox(self.color_pattern_frame, height=10)
        self.color_listbox.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

        self.pattern_listbox = tk.Listbox(self.color_pattern_frame, height=10)
        self.pattern_listbox.grid(column=1, row=0, padx=10, pady=10, sticky='nsew')

        # Textures Section
        self.texture_frame = ttk.LabelFrame(self, text="Textures")
        self.texture_frame.grid(column=4, row=1, padx=10, pady=10, sticky='ew')

        self.texture_listbox = tk.Listbox(self.texture_frame, height=10)
        self.texture_listbox.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

        # Save Button
        self.save_button = ttk.Button(self, text="Create Ticket", command=self.save_ticket)
        self.save_button.grid(column=0, row=2, columnspan=5, padx=10, pady=10, sticky='ew')

    def load_ticket_type_details(self):
        cursor = self.db_conn.cursor()

        # Load Garments
        cursor.execute("SELECT id, name FROM garments WHERE id IN (SELECT garment_id FROM ticket_type_garments WHERE ticket_type_id = ?)", (self.ticket_type_id,))
        self.garments = cursor.fetchall()
        for garment in self.garments:
            self.garment_listbox.insert(tk.END, garment[1])

        # Load Colors
        cursor.execute("SELECT id, name FROM colors WHERE id IN (SELECT color_id FROM ticket_type_colors WHERE ticket_type_id = ?)", (self.ticket_type_id,))
        self.colors = cursor.fetchall()
        for color in self.colors:
            self.color_listbox.insert(tk.END, color[1])

        # Load Patterns
        cursor.execute("SELECT id, name FROM patterns WHERE id IN (SELECT pattern_id FROM ticket_type_patterns WHERE ticket_type_id = ?)", (self.ticket_type_id,))
        self.patterns = cursor.fetchall()
        for pattern in self.patterns:
            self.pattern_listbox.insert(tk.END, pattern[1])

        # Load Textures
        cursor.execute("SELECT id, name FROM textures WHERE id IN (SELECT texture_id FROM ticket_type_textures WHERE ticket_type_id = ?)", (self.ticket_type_id,))
        self.textures = cursor.fetchall()
        for texture in self.textures:
            self.texture_listbox.insert(tk.END, texture[1])

        # Load Upcharges
        cursor.execute("SELECT id, name FROM upcharges WHERE id IN (SELECT upcharge_id FROM ticket_type_upcharges WHERE ticket_type_id = ?)", (self.ticket_type_id,))
        self.upcharges = cursor.fetchall()
        for upcharge in self.upcharges:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.upcharge_frame, text=upcharge[1], variable=var)
            chk.pack(anchor='w')
            self.upcharge_vars[upcharge[1]] = var

    def save_ticket(self):
        cursor = self.db_conn.cursor()

        # Insert the new ticket into the tickets table
        cursor.execute('''
            INSERT INTO tickets (customer_id, date, ticket_number, rack, pieces, total, status, type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.customer_id,
            self.drop_date.get(),
            self.generate_ticket_number(),
            "",  # Assuming rack info will be added later
            0,   # Assuming pieces count will be added later
            0.0,  # Assuming total price will be added later
            "Pending",  # Default status
            "Detailed"  # Ticket type
    ))

        ticket_id = cursor.lastrowid  # Get the ID of the newly inserted ticket

        # Insert the selected garments into the ticket_items table
        for garment in self.garment_listbox.get(0, tk.END):
            cursor.execute('''
            INSERT INTO ticket_items (ticket_id, garment_id, variant_id, quantity, price)
            VALUES (?, (SELECT id FROM garments WHERE name = ?), 0, 1, 0.0)
        ''', (
            ticket_id,
            garment
        ))

        # Insert the selected upcharges into the ticket_items table
        for upcharge, var in self.upcharge_vars.items():
            if var.get():
                cursor.execute('''
                INSERT INTO ticket_items (ticket_id, garment_id, variant_id, quantity, price)
                VALUES (?, 0, (SELECT id FROM upcharges WHERE name = ?), 1, 0.0)
            ''', (
                ticket_id,
                upcharge
            ))

        self.db_conn.commit()
        self.parent.update_ticket_list()
        self.destroy()

    def generate_ticket_number(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT MAX(ticket_number) FROM tickets")
        max_ticket_number = cursor.fetchone()[0]
        if max_ticket_number is None:
            return 1
        else:
            return max_ticket_number + 1

if __name__ == "__main__":
    def create_db_connection():
        conn = sqlite3.connect('pos_system.db')
        return conn

    db_conn = create_db_connection()

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = DetailedTicketCreationWindow(root, db_conn, customer_id=1, ticket_type_id=1)
    app.mainloop()
