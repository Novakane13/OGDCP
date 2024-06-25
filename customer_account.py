import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import requests
from ticket_type import TicketTypeWindow

class CustomerAccountWindow(tk.Toplevel):
    def __init__(self, parent, db_conn, customer_id=None):
        super().__init__(parent)
        self.db_conn = db_conn
        self.customer_id = customer_id
        self.title("Ogden's Dry Clean Program")
        self.geometry("2000x1200")  # Set a default size for the window
        self.create_widgets()
        self.load_ticket_types()
        if self.customer_id:
            self.load_customer_data()

    def create_widgets(self):
        # Next Customer Button
        self.next_customer_button = ttk.Button(self, text="Next Customer", command=self.next_customer)
        self.next_customer_button.grid(column=0, row=0, padx=10, pady=10, sticky='w')

        # Customer Information
        self.customer_info_frame = ttk.LabelFrame(self, text="Customer Information")
        self.customer_info_frame.grid(column=0, row=1, padx=10, pady=10, sticky='w')

        ttk.Label(self.customer_info_frame, text="Last Name:").grid(column=0, row=0, padx=5, pady=5, sticky='w')
        self.last_name_entry = ttk.Entry(self.customer_info_frame)
        self.last_name_entry.grid(column=1, row=0, padx=5, pady=5, sticky='w')
        self.last_name_entry.bind("<FocusOut>", self.save_customer_data)

        ttk.Label(self.customer_info_frame, text="First Name:").grid(column=0, row=1, padx=5, pady=5, sticky='w')
        self.first_name_entry = ttk.Entry(self.customer_info_frame)
        self.first_name_entry.grid(column=1, row=1, padx=5, pady=5, sticky='w')
        self.first_name_entry.bind("<FocusOut>", self.save_customer_data)

        ttk.Label(self.customer_info_frame, text="Phone #:").grid(column=0, row=2, padx=5, pady=5, sticky='w')
        self.phone_entry = ttk.Entry(self.customer_info_frame)
        self.phone_entry.grid(column=1, row=2, padx=5, pady=5, sticky='w')
        self.phone_entry.bind("<FocusOut>", self.save_customer_data)

        ttk.Label(self.customer_info_frame, text="Notes:").grid(column=0, row=3, padx=5, pady=5, sticky='nw')
        self.notes_text = tk.Text(self.customer_info_frame, width=30, height=4)
        self.notes_text.grid(column=1, row=3, padx=5, pady=5, sticky='w')
        self.notes_text.bind("<FocusOut>", self.save_customer_data)

        # Buttons for Ticket Types
        self.ticket_type_buttons_frame = ttk.Frame(self)
        self.ticket_type_buttons_frame.grid(column=0, row=2, padx=10, pady=5, sticky='nsew')

        # Tickets
        columns = ("ticket_id", "customer_id", "date", "ticket_number", "rack", "pieces", "total", "status", "type")
        self.tickets_tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tickets_tree.grid(column=1, row=0, rowspan=3, padx=10, pady=10, sticky='nsew')

        for col in columns:
            self.tickets_tree.heading(col, text=col.replace("_", " ").title())
            self.tickets_tree.column(col, width=100)

        # Configure the grid to make the ticket list window twice as tall
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)

        # Buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(column=2, row=0, rowspan=3, padx=10, pady=10, sticky='ns')

        buttons = [
            "View Ticket", "Edit Ticket", "Redo Ticket", "Void Ticket",
            "Assign Tags", "Undo Pickup", "Reprint Cust. Receipt",
            "Reprint Ticket", "Print Tags"
        ]
        for button in buttons:
            ttk.Button(self.buttons_frame, text=button, command=lambda b=button: self.handle_button_click(b)).pack(pady=5, fill='x')

        # Frame for ticket type buttons
        self.ticket_buttons_frame = tk.Frame(self)
        self.ticket_buttons_frame.grid(column=0, row=2, padx=10, pady=10, sticky='nsew')

        # Configure grid for buttons
        self.ticket_buttons_frame.grid_columnconfigure(0, weight=1)
        self.ticket_buttons_frame.grid_columnconfigure(1, weight=1)
        self.ticket_buttons_frame.grid_columnconfigure(2, weight=1)

        # Create ticket type buttons
        self.create_ticket_type_buttons()

    def next_customer(self):
        # Placeholder for next customer functionality
        messagebox.showinfo("Next Customer", "Next customer functionality not yet implemented.")

    def handle_button_click(self, button):
        # Placeholder for handling button clicks
        messagebox.showinfo(button, f"{button} functionality not yet implemented.")

    def load_customer_data(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT last_name, first_name, phone, notes FROM customers WHERE id = ?", (self.customer_id,))
        customer = cursor.fetchone()

        if customer:
            self.last_name_entry.insert(0, customer[0])
            self.first_name_entry.insert(0, customer[1])
            self.phone_entry.insert(0, customer[2])
            self.notes_text.insert(tk.END, customer[3])

    def save_customer_data(self, event=None):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        phone = self.phone_entry.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        cursor = self.db_conn.cursor()

        if self.customer_id:
            cursor.execute('''
                UPDATE customers
                SET last_name = ?, first_name = ?, phone = ?, notes = ?
                WHERE id = ?
            ''', (last_name, first_name, phone, notes, self.customer_id))
        else:
            cursor.execute('''
                INSERT INTO customers (last_name, first_name, phone, notes)
                VALUES (?, ?, ?, ?)
            ''', (last_name, first_name, phone, notes))
            self.customer_id = cursor.lastrowid

        self.db_conn.commit()

    def create_ticket_type_buttons(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, name FROM ticket_types")
        ticket_types = cursor.fetchall()

        row = 0
        col = 0

        for ticket_type_id, ticket_type_name in ticket_types:
            button = ttk.Button(self.ticket_buttons_frame, text=ticket_type_name, command=lambda id=ticket_type_id: self.open_ticket_creation_window(id))
            button.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def open_ticket_creation_window(self, ticket_type_id):
        TicketCreationWindow(self, self.db_conn, self.customer_id, ticket_type_id)

    def load_ticket_types(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, name FROM ticket_types")
        ticket_types = cursor.fetchall()

        for ticket_type in ticket_types:
            button = ttk.Button(self.ticket_type_buttons_frame, text=ticket_type[1], command=lambda tt=ticket_type: self.create_ticket(tt))
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_ticket(self, ticket_type):
        TicketCreationWindow(self, self.db_conn, self.customer_id, ticket_type[0])

class TicketCreationWindow(tk.Toplevel):
    def __init__(self, parent, db_conn, customer_id, ticket_type_id):
        super().__init__(parent)
        self.db_conn = db_conn
        self.customer_id = customer_id
        self.ticket_type_id = ticket_type_id
        self.title("Create Ticket")
        self.geometry("800x600")
        self.create_widgets()
        self.load_ticket_type_details()

    def create_widgets(self):
        # Ticket Window
        self.ticket_window_frame = tk.Frame(self, relief=tk.SUNKEN, borderwidth=1)
        self.ticket_window_frame.place(x=20, y=20, width=350, height=500)

        self.ticket_window_label = tk.Label(self.ticket_window_frame, text="Ticket Window", font=("Arial", 12))
        self.ticket_window_label.pack(anchor=tk.N, pady=10)

        self.ticket_window = tk.Listbox(self.ticket_window_frame)
        self.ticket_window.pack(expand=True, fill=tk.BOTH)

        # Garment Selection Frame
        self.garment_frame = tk.Frame(self, relief=tk.SUNKEN, borderwidth=1)
        self.garment_frame.place(x=380, y=20, width=400, height=500)

        self.garment_label = tk.Label(self.garment_frame, text="Select Garment", font=("Arial", 12))
        self.garment_label.pack(anchor=tk.N, pady=10)

        self.garment_list = tk.Listbox(self.garment_frame)
        self.garment_list.pack(expand=True, fill=tk.BOTH)

        # Complete Ticket Button
        self.complete_ticket_button = tk.Button(self, text="Complete Ticket", command=self.complete_ticket)
        self.complete_ticket_button.pack(side=tk.BOTTOM, pady=20)

        # Total Price
        self.total_price_label = tk.Label(self, text="Total: $0.00", font=("Arial", 12))
        self.total_price_label.pack(side=tk.BOTTOM)

    def load_ticket_type_details(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT garment_id FROM ticket_type_garments WHERE ticket_type_id = ?", (self.ticket_type_id,))
        garment_ids = [row[0] for row in cursor.fetchall()]

        if garment_ids:
            for garment_id in garment_ids:
                cursor.execute("SELECT name, image FROM garments WHERE id = ?", (garment_id,))
                garment = cursor.fetchone()
                if garment:
                    self.garment_list.insert(tk.END, garment[0])

        self.garment_list.bind('<Double-1>', self.show_variants)

    def show_variants(self, event):
        selected_index = self.garment_list.curselection()[0]
        selected_garment = self.garment_list.get(selected_index)
        
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id FROM garments WHERE name = ?", (selected_garment,))
        garment_id = cursor.fetchone()[0]
        cursor.execute("SELECT id, name, price FROM variations WHERE garment_id = ?", (garment_id,))
        variants = cursor.fetchall()

        variant_window = tk.Toplevel(self)
        variant_window.title("Select Variant")
        variant_window.geometry("300x200")

        variant_listbox = tk.Listbox(variant_window)
        variant_listbox.pack(expand=True, fill=tk.BOTH)

        for variant in variants:
            variant_listbox.insert(tk.END, f"{variant[1]} - ${variant[2]}")

        def select_variant():
            selected_variant_index = variant_listbox.curselection()[0]
            selected_variant = variants[selected_variant_index]
            self.add_garment_to_ticket(selected_garment, selected_variant)
            variant_window.destroy()

        select_button = tk.Button(variant_window, text="Select", command=select_variant)
        select_button.pack(pady=10)

    def add_garment_to_ticket(self, garment_name, variant):
        self.ticket_window.insert(tk.END, f"{garment_name} - {variant[1]} - ${variant[2]}")
        self.update_total_price()

    def update_total_price(self):
        total = 0.0
        for i in range(self.ticket_window.size()):
            item = self.ticket_window.get(i)
            price = float(item.split('- $')[1])
            total += price
        self.total_price_label.config(text=f"Total: ${total:.2f}")

    def complete_ticket(self):
        ticket_items = []
        for i in range(self.ticket_window.size()):
            item = self.ticket_window.get(i)
            garment_name, variant_name, price = item.split(' - ')
            price = float(price.split('$')[1])
            ticket_items.append((garment_name, variant_name, price))

        cursor = self.db_conn.cursor()

        cursor.execute("SELECT MAX(ticket_number) FROM tickets")
        max_ticket_number = cursor.fetchone()[0]
        if max_ticket_number is None:
            max_ticket_number = 0
        new_ticket_number = max_ticket_number + 1

        cursor.execute("INSERT INTO tickets (customer_id, ticket_number, date, total, status) VALUES (?, ?, DATE('now'), ?, 'open')",
                       (self.customer_id, new_ticket_number, sum(item[2] for item in ticket_items)))
        ticket_id = cursor.lastrowid

        for garment_name, variant_name, price in ticket_items:
            cursor.execute("SELECT id FROM garments WHERE name = ?", (garment_name,))
            garment_id = cursor.fetchone()[0]
            cursor.execute("SELECT id FROM variations WHERE name = ?", (variant_name,))
            variant_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO ticket_items (ticket_id, garment_id, variant_id, quantity, price) VALUES (?, ?, ?, ?, ?)",
                           (ticket_id, garment_id, variant_id, 1, price))  # Assuming quantity as 1 for simplicity

        self.db_conn.commit()

        messagebox.showinfo("Ticket Created", f"Ticket created successfully! Ticket number: {new_ticket_number}")
        self.destroy()


class QuickTicketWindow(tk.Toplevel):
    def __init__(self, parent, db_conn, customer_id):
        super().__init__(parent)
        self.db_conn = db_conn
        self.customer_id = customer_id
        self.title("Create Quick Ticket")
        self.geometry("400x500")
        self.create_widgets()
        self.load_ticket_types()

    def create_widgets(self):
        tk.Label(self, text="Quick Ticket", font=("Arial", 16)).pack(pady=10)

        # Due Date
        tk.Label(self, text="Due Date").pack()
        self.due_date = DateEntry(self, width=20, background='darkblue', foreground='white', borderwidth=2)
        self.due_date.pack(pady=5)

        # Ticket Type, Pieces, and Notes
        self.ticket_frame = tk.Frame(self)
        self.ticket_frame.pack(pady=10)

        for i in range(3):
            tk.Label(self.ticket_frame, text="Ticket Type").grid(row=i, column=0, padx=5, pady=5)
            tk.Label(self.ticket_frame, text="# of Items").grid(row=i, column=1, padx=5, pady=5)
            tk.Label(self.ticket_frame, text="Notes for this ticket type").grid(row=i, column=2, padx=5, pady=5)
            setattr(self, f"ticket_type_{i+1}", ttk.Combobox(self.ticket_frame, width=20))
            getattr(self, f"ticket_type_{i+1}").grid(row=i, column=0, padx=5, pady=5)
            setattr(self, f"pieces_{i+1}", tk.Spinbox(self.ticket_frame, from_=1, to=100, width=5))
            getattr(self, f"pieces_{i+1}").grid(row=i, column=1, padx=5, pady=5)
            setattr(self, f"notes_{i+1}", tk.Entry(self.ticket_frame, width=20))
            getattr(self, f"notes_{i+1}").grid(row=i, column=2, padx=5, pady=5)

        # Overall Notes
        tk.Label(self, text="Notes for Quick Ticket").pack()
        self.overall_notes = tk.Entry(self, width=40)
        self.overall_notes.pack(pady=5)

        # Submit Button
        tk.Button(self, text="Create Quick Ticket", command=self.submit_quick_ticket).pack(pady=20)

    def load_ticket_types(self):
        try:
            response = requests.get('http://127.0.0.1:5000/ticket_types')
            if response.status_code == 200:
                ticket_types = response.json()
                for i in range(3):
                    combobox = getattr(self, f"ticket_type_{i+1}")
                    combobox['values'] = [ticket_type['name'] for ticket_type in ticket_types]
            else:
                messagebox.showerror("Error", "Failed to load ticket types.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to the server: {e}")

    def submit_quick_ticket(self):
        quick_ticket = {
            "customer_id": self.customer_id,
            "due_date": self.due_date.get(),
            "tickets": [
                {
                    "ticket_type": getattr(self, "ticket_type_1").get(),
                    "pieces": getattr(self, "pieces_1").get(),
                    "notes": getattr(self, "notes_1").get()
                },
                {
                    "ticket_type": getattr(self, "ticket_type_2").get(),
                    "pieces": getattr(self, "pieces_2").get(),
                    "notes": getattr(self, "notes_2").get()
                },
                {
                    "ticket_type": getattr(self, "ticket_type_3").get(),
                    "pieces": getattr(self, "pieces_3").get(),
                    "notes": getattr(self, "notes_3").get()
                }
            ],
            "overall_notes": self.overall_notes.get()
        }

        try:
            response = requests.post('http://127.0.0.1:5000/quick_tickets', json=quick_ticket)
            if response.status_code == 201:
                messagebox.showinfo("Success", "Quick Ticket created successfully!")
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to create Quick Ticket.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to the server: {e}")

if __name__ == "__main__":
    def create_db_connection(db_path='pos_system.db'):
        conn = sqlite3.connect(db_path)
        return conn

    db_conn = create_db_connection()

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = CustomerAccountWindow(root, db_conn)
    app.mainloop()
