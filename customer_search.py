import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from customer_account import CustomerAccountWindow
from initialize_db import create_db_connection

class CustomerSearchWindow(tk.Toplevel):
    def __init__(self, parent, db_conn):
        super().__init__(parent)
        self.db_conn = db_conn
        self.title("Search Customer")
        self.geometry("600x400")  # Set a default size for the window
        self.create_widgets()
    
    def create_widgets(self):
        # Input fields
        ttk.Label(self, text="Last Name:").grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.last_name_entry = ttk.Entry(self)
        self.last_name_entry.grid(column=0, row=1, padx=10, pady=5, sticky='w')
        self.last_name_entry.bind("<Return>", lambda event: self.search_customers())

        ttk.Label(self, text="First Name:").grid(column=0, row=2, padx=10, pady=5, sticky='w')
        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.grid(column=0, row=3, padx=10, pady=5, sticky='w')
        self.first_name_entry.bind("<Return>", lambda event: self.search_customers())

        ttk.Label(self, text="Phone #:").grid(column=0, row=4, padx=10, pady=5, sticky='w')
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(column=0, row=5, padx=10, pady=5, sticky='w')
        self.phone_entry.bind("<Return>", lambda event: self.search_customers())

        # Search results listbox
        ttk.Label(self, text="Customer Name").grid(column=1, row=0, padx=10, pady=5, sticky='w')
        ttk.Label(self, text="Phone").grid(column=2, row=0, padx=10, pady=5, sticky='w')
        self.result_list = tk.Listbox(self, height=15, width=50)
        self.result_list.grid(column=1, row=1, rowspan=6, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.result_list.bind("<Double-1>", lambda event: self.select_customer())
        
        # Buttons
        self.new_customer_button = ttk.Button(self, text="New Customer", command=self.create_new_customer)
        self.new_customer_button.grid(column=0, row=7, padx=10, pady=10, sticky='w')
        
        self.search_button = ttk.Button(self, text="OK", command=self.search_customers)
        self.search_button.grid(column=1, row=7, padx=10, pady=10, sticky='e')

        self.close_button = ttk.Button(self, text="Cancel", command=self.destroy)
        self.close_button.grid(column=2, row=7, padx=10, pady=10, sticky='e')

    def search_customers(self):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        phone = self.phone_entry.get()

        query = "SELECT id, last_name, first_name, phone FROM customers WHERE 1=1"
        params = []

        if last_name:
            query += " AND last_name LIKE ?"
            params.append(f"%{last_name}%")
        if first_name:
            query += " AND first_name LIKE ?"
            params.append(f"%{first_name}%")
        if phone:
            query += " AND phone LIKE ?"
            params.append(f"%{phone}%")

        cursor = self.db_conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()

        self.result_list.delete(0, tk.END)
        for customer in results:
            self.result_list.insert(tk.END, f"{customer[1]} {customer[2]} - {customer[3]}")

    def select_customer(self):
        selection = self.result_list.get(self.result_list.curselection())
        customer_name, phone = selection.split(" - ")
        last_name, first_name = customer_name.split(" ", 1)

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id FROM customers WHERE last_name = ? AND first_name = ? AND phone = ?", (last_name, first_name, phone))
        customer_id = cursor.fetchone()[0]

        self.destroy()
        CustomerAccountWindow(self.master, self.db_conn, customer_id)

    def create_new_customer(self):
        self.destroy()
        CustomerAccountWindow(self.master, self.db_conn)

if __name__ == "__main__":
    # Create or connect to your database using the initialize_db function
    db_conn = create_db_connection()

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    customer_search_app = CustomerSearchWindow(root, db_conn)
    customer_search_app.mainloop()
