import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class QuickTicketWindow(tk.Toplevel):
    def __init__(self, parent, db_conn):
        super().__init__(parent)
        self.db_conn = db_conn
        self.title("Quick Ticket")
        self.geometry("400x500")  # Adjust the size as needed

        self.create_widgets()

    def create_widgets(self):
        # Due Date
        ttk.Label(self, text="Due Date").grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.due_date_entry = ttk.Entry(self)
        self.due_date_entry.grid(column=1, row=0, padx=10, pady=5, sticky='w')

        # Ticket Items
        self.items_frame = ttk.LabelFrame(self, text="Items")
        self.items_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=5, sticky='nsew')

        self.item_entries = []
        for i in range(3):
            item_frame = ttk.Frame(self.items_frame)
            item_frame.grid(column=0, row=i, padx=5, pady=5, sticky='w')

            ticket_type_label = ttk.Label(item_frame, text=f"Ticket Type {i+1}")
            ticket_type_label.grid(column=0, row=0, padx=5, pady=5, sticky='w')

            ticket_type_combobox = ttk.Combobox(item_frame, state="readonly")
            ticket_type_combobox['values'] = self.get_ticket_types()
            ticket_type_combobox.grid(column=1, row=0, padx=5, pady=5, sticky='w')

            pieces_entry = ttk.Entry(item_frame)
            pieces_entry.grid(column=2, row=0, padx=5, pady=5, sticky='w')

            notes_entry = ttk.Entry(item_frame)
            notes_entry.grid(column=3, row=0, padx=5, pady=5, sticky='w')

            self.item_entries.append((ticket_type_combobox, pieces_entry, notes_entry))

        # Overall Notes
        ttk.Label(self, text="Overall Notes").grid(column=0, row=2, padx=10, pady=5, sticky='w')
        self.notes_text = tk.Text(self, height=4)
        self.notes_text.grid(column=0, row=3, columnspan=2, padx=10, pady=5, sticky='nsew')

        # Create Button
        self.create_button = ttk.Button(self, text="Create Quick Ticket", command=self.create_quick_ticket)
        self.create_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10, sticky='ew')

    def get_ticket_types(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT name FROM ticket_types")
        ticket_types = [row[0] for row in cursor.fetchall()]
        return ticket_types

    def create_quick_ticket(self):
        due_date = self.due_date_entry.get()
        overall_notes = self.notes_text.get("1.0", tk.END).strip()

        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO quick_tickets (due_date, overall_notes) VALUES (?, ?)", (due_date, overall_notes))
        quick_ticket_id = cursor.lastrowid

        for ticket_type_combobox, pieces_entry, notes_entry in self.item_entries:
            ticket_type = ticket_type_combobox.get()
            pieces = pieces_entry.get()
            notes = notes_entry.get()

            if ticket_type and pieces:
                cursor.execute("INSERT INTO quick_ticket_items (quick_ticket_id, ticket_type, pieces, notes) VALUES (?, ?, ?, ?)",
                               (quick_ticket_id, ticket_type, pieces, notes))

        self.db_conn.commit()
        messagebox.showinfo("Success", "Quick ticket created successfully.")
        self.destroy()

if __name__ == "__main__":
    def create_db_connection(db_path='pos_system.db'):
        conn = sqlite3.connect(db_path)
        return conn

    db_conn = create_db_connection()

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = QuickTicketWindow(root, db_conn)
    app.mainloop()
