import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class TicketTypeWindow(tk.Toplevel):
    def __init__(self, parent, db_conn, ticket_type_id=None):
        super().__init__(parent)
        self.db_conn = db_conn
        self.ticket_type_id = ticket_type_id
        self.title("Ticket Type Creation/Edit")
        self.geometry("2000x1200")  # Set a default size for the window
        self.create_widgets()
        self.refresh_lists()
        if self.ticket_type_id:
            self.load_ticket_type_data()

    def create_widgets(self):
        # Name of Ticket Type
        ttk.Label(self, text="Name of Ticket Type").grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.ticket_type_entry = ttk.Entry(self)
        self.ticket_type_entry.grid(column=1, row=0, padx=10, pady=5, sticky='w')

        # Large Empty Box for Garment Selection
        self.garment_selection_frame = ttk.LabelFrame(self, text="Garments for this ticket type", relief=tk.SUNKEN, borderwidth=1)
        self.garment_selection_frame.grid(column=0, row=1, columnspan=2, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.garment_selection_frame.grid_propagate(False)
        self.garment_selection_frame.config(width=300, height=400)
        self.selected_garments_listbox = tk.Listbox(self.garment_selection_frame)
        self.selected_garments_listbox.pack(fill=tk.BOTH, expand=True)
        self.selected_garments_listbox.bind("<Button-3>", self.show_garment_context_menu)

        # Garments List
        self.garment_list_frame = ttk.LabelFrame(self, text="Garment List")
        self.garment_list_frame.grid(column=2, row=1, padx=10, pady=10, sticky='nsew')
        self.garments_listbox = tk.Listbox(self.garment_list_frame)
        self.garments_listbox.pack(fill=tk.BOTH, expand=True)
        self.garments_listbox.bind("<Double-1>", self.add_selected_garment)

        # Colors with Checkboxes
        self.color_list_frame = ttk.LabelFrame(self, text="Colors List")
        self.color_list_frame.grid(column=3, row=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Patterns with Checkboxes
        self.pattern_list_frame = ttk.LabelFrame(self, text="Patterns List")
        self.pattern_list_frame.grid(column=4, row=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Upcharges with Checkboxes
        self.upcharges_list_frame = ttk.LabelFrame(self, text="Upcharges List")
        self.upcharges_list_frame.grid(column=5, row=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Discounts/Coupons with Checkboxes
        self.coupons_discounts_list_frame = ttk.LabelFrame(self, text="Discounts/Coupons List")
        self.coupons_discounts_list_frame.grid(column=6, row=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Textures with Checkboxes
        self.textures_list_frame = ttk.LabelFrame(self, text="Textures List")
        self.textures_list_frame.grid(column=7, row=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Save Button
        self.save_button = ttk.Button(self, text="Save Ticket Type", command=self.save_ticket_type)
        self.save_button.grid(column=0, row=8, columnspan=8, padx=10, pady=10, sticky='ew')

        # Ticket Types List Frame
        self.ticket_types_frame = ttk.LabelFrame(self, text="Saved Ticket Types")
        self.ticket_types_frame.grid(column=0, row=9, columnspan=8, padx=10, pady=10, sticky="nsew")
        self.ticket_types_listbox = tk.Listbox(self.ticket_types_frame)
        self.ticket_types_listbox.pack(fill=tk.BOTH, expand=True)
        self.ticket_types_listbox.bind("<Double-1>", self.edit_ticket_type)
        self.edit_button = ttk.Button(self.ticket_types_frame, text="Edit Selected", command=self.edit_selected_item)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button = ttk.Button(self.ticket_types_frame, text="Delete Selected", command=self.delete_selected_item)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Context menu for removing selected garments
        self.garment_context_menu = tk.Menu(self, tearoff=0)
        self.garment_context_menu.add_command(label="Remove", command=self.remove_selected_garment)

    def refresh_lists(self):
        self.refresh_color_list()
        self.refresh_garment_list()
        self.refresh_pattern_list()
        self.refresh_coupons_discounts_list()
        self.refresh_upcharges_list()
        self.refresh_textures_list()
        self.refresh_ticket_types_list()

    def refresh_color_list(self):
        self.clear_frame(self.color_list_frame)
        self.colors = self.create_checkboxes_list(self.color_list_frame, "SELECT id, name FROM colors")

    def refresh_garment_list(self):
        self.garments_listbox.delete(0, tk.END)
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, name, image FROM garments")
        self.garments = cursor.fetchall()
        for garment in self.garments:
            self.garments_listbox.insert(tk.END, garment[1])

    def refresh_pattern_list(self):
        self.clear_frame(self.pattern_list_frame)
        self.patterns = self.create_checkboxes_list(self.pattern_list_frame, "SELECT id, name FROM patterns")

    def refresh_coupons_discounts_list(self):
        self.clear_frame(self.coupons_discounts_list_frame)
        self.coupons_discounts = self.create_checkboxes_list(self.coupons_discounts_list_frame, "SELECT id, name FROM coupons_discounts")

    def refresh_upcharges_list(self):
        self.clear_frame(self.upcharges_list_frame)
        self.upcharges = self.create_checkboxes_list(self.upcharges_list_frame, "SELECT id, name FROM upcharges")

    def refresh_textures_list(self):
        self.clear_frame(self.textures_list_frame)
        self.textures = self.create_checkboxes_list(self.textures_list_frame, "SELECT id, name FROM textures")

    def refresh_ticket_types_list(self):
        self.ticket_types_listbox.delete(0, tk.END)
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, name FROM ticket_types")
        self.ticket_types = cursor.fetchall()
        for ticket_type in self.ticket_types:
            self.ticket_types_listbox.insert(tk.END, ticket_type[1])

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def create_checkboxes_list(self, frame, query):
        cursor = self.db_conn.cursor()
        cursor.execute(query)
        items = cursor.fetchall()
        checkboxes = []
        for item in items:
            var = tk.BooleanVar()
            text = item[1]
            cb = ttk.Checkbutton(frame, text=text, variable=var)
            cb.pack(anchor='w')
            checkboxes.append((item[0], var))  # Store id and variable
        return checkboxes

    def add_selected_garment(self, event):
        selection = self.garments_listbox.curselection()
        if selection:
            index = selection[0]
            garment_id, garment_name, garment_image = self.garments[index]
            self.show_pricing_popup(garment_id, garment_name, garment_image)

    def show_pricing_popup(self, garment_id, garment_name, garment_image):
        pricing_window = tk.Toplevel(self)
        pricing_window.title("Set Prices for Garment Variations")
        ttk.Label(pricing_window, text=f"Set Prices for {garment_name}").grid(column=0, row=0, columnspan=2, padx=10, pady=10)
        image = Image.open(garment_image)
        image.thumbnail((50, 50))
        photo = ImageTk.PhotoImage(image)
        image_label = ttk.Label(pricing_window, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

        # Price input for the original garment
        ttk.Label(pricing_window, text=f"{garment_name} Price").grid(column=0, row=2, padx=10, pady=5, sticky='w')
        original_price_var = tk.StringVar()
        ttk.Entry(pricing_window, textvariable=original_price_var).grid(column=1, row=2, padx=10, pady=5)
        price_vars = [(None, original_price_var)]  # Add the original garment price var to the list

        # Get garment variations from the database
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, name FROM variations WHERE garment_id = ?", (garment_id,))
        variations = cursor.fetchall()

        row = 3
        for variation_id, variation_name in variations:
            ttk.Label(pricing_window, text=f"{variation_name} Price").grid(column=0, row=row, padx=10, pady=5, sticky='w')
            variation_price_var = tk.StringVar()
            ttk.Entry(pricing_window, textvariable=variation_price_var).grid(column=1, row=row, padx=10, pady=5)
            price_vars.append((variation_id, variation_price_var))
            row += 1

        def save_prices():
            cursor = self.db_conn.cursor()
            for variation_id, price_var in price_vars:
                price = price_var.get()
                if variation_id is None:  # Original garment price
                    cursor.execute('''
                        INSERT OR REPLACE INTO garment_prices (garment_id, price)
                        VALUES (?, ?)
                    ''', (garment_id, price))
                else:  # Variation prices
                    cursor.execute('''
                        INSERT OR REPLACE INTO variation_prices (variation_id, price)
                        VALUES (?, ?)
                    ''', (variation_id, price))
            self.db_conn.commit()
            pricing_window.destroy()

        save_button = ttk.Button(pricing_window, text="Save Prices", command=save_prices)
        save_button.grid(column=0, row=row, columnspan=2, padx=10, pady=10)

    def remove_selected_garment(self):
        selection = self.selected_garments_listbox.curselection()
        if selection:
            self.selected_garments_listbox.delete(selection[0])

    def show_garment_context_menu(self, event):
        self.garment_context_menu.tk_popup(event.x_root, event.y_root)

    def save_ticket_type(self):
        ticket_type_name = self.ticket_type_entry.get()
        if not ticket_type_name:
            messagebox.showerror("Error", "Please enter a name for the ticket type.")
            return

        cursor = self.db_conn.cursor()
        if self.ticket_type_id:
            cursor.execute('''
                UPDATE ticket_types
                SET name = ?
                WHERE id = ?
            ''', (ticket_type_name, self.ticket_type_id))
            cursor.execute('DELETE FROM ticket_type_garments WHERE ticket_type_id = ?', (self.ticket_type_id,))
            cursor.execute('DELETE FROM ticket_type_colors WHERE ticket_type_id = ?', (self.ticket_type_id,))
            cursor.execute('DELETE FROM ticket_type_patterns WHERE ticket_type_id = ?', (self.ticket_type_id,))
            cursor.execute('DELETE FROM ticket_type_upcharges WHERE ticket_type_id = ?', (self.ticket_type_id,))
            cursor.execute('DELETE FROM ticket_type_coupons_discounts WHERE ticket_type_id = ?', (self.ticket_type_id,))
            cursor.execute('DELETE FROM ticket_type_textures WHERE ticket_type_id = ?', (self.ticket_type_id,))
        else:
            cursor.execute('INSERT INTO ticket_types (name) VALUES (?)', (ticket_type_name,))
            self.ticket_type_id = cursor.lastrowid

        # Save selected garments
        selected_garments = self.selected_garments_listbox.get(0, tk.END)
        for garment in selected_garments:
            cursor.execute('SELECT id FROM garments WHERE name = ?', (garment,))
            garment_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO ticket_type_garments (ticket_type_id, garment_id) VALUES (?, ?)', (self.ticket_type_id, garment_id))

        # Save selected colors
        for color_id, var in self.colors:
            if var.get():
                cursor.execute('INSERT INTO ticket_type_colors (ticket_type_id, color_id) VALUES (?, ?)', (self.ticket_type_id, color_id))

        # Save selected patterns
        for pattern_id, var in self.patterns:
            if var.get():
                cursor.execute('INSERT INTO ticket_type_patterns (ticket_type_id, pattern_id) VALUES (?, ?)', (self.ticket_type_id, pattern_id))

        # Save selected upcharges
        for upcharge_id, var in self.upcharges:
            if var.get():
                cursor.execute('INSERT INTO ticket_type_upcharges (ticket_type_id, upcharge_id) VALUES (?, ?)', (self.ticket_type_id, upcharge_id))

        # Save selected coupons_discounts
        for coupon_discount_id, var in self.coupons_discounts:
            if var.get():
                cursor.execute('INSERT INTO ticket_type_coupons_discounts (ticket_type_id, coupon_discount_id) VALUES (?, ?)', (self.ticket_type_id, coupon_discount_id))

        # Save selected textures
        for texture_id, var in self.textures:
            if var.get():
                cursor.execute('INSERT INTO ticket_type_textures (ticket_type_id, texture_id) VALUES (?, ?)', (self.ticket_type_id, texture_id))

        self.db_conn.commit()
        self.refresh_ticket_types_list()
        messagebox.showinfo("Success", "Ticket type saved successfully.")
        self.destroy()

    def load_ticket_type_data(self):
        cursor = self.db_conn.cursor()
        cursor.execute('SELECT name FROM ticket_types WHERE id = ?', (self.ticket_type_id,))
        ticket_type_name = cursor.fetchone()[0]
        self.ticket_type_entry.insert(0, ticket_type_name)

        cursor.execute('SELECT garment_id FROM ticket_type_garments WHERE ticket_type_id = ?', (self.ticket_type_id,))
        garment_ids = cursor.fetchall()
        for garment_id in garment_ids:
            cursor.execute('SELECT name FROM garments WHERE id = ?', (garment_id[0],))
            garment_name = cursor.fetchone()[0]
            self.selected_garments_listbox.insert(tk.END, garment_name)

        self.load_checked_items('ticket_type_colors', self.colors)
        self.load_checked_items('ticket_type_patterns', self.patterns)
        self.load_checked_items('ticket_type_upcharges', self.upcharges)
        self.load_checked_items('ticket_type_coupons_discounts', self.coupons_discounts)
        self.load_checked_items('ticket_type_textures', self.textures)

    def load_checked_items(self, table_name, items):
        cursor = self.db_conn.cursor()
        cursor.execute(f'SELECT {table_name[:-1]}_id FROM {table_name} WHERE ticket_type_id = ?', (self.ticket_type_id,))
        selected_ids = cursor.fetchall()
        selected_ids = [id_tuple[0] for id_tuple in selected_ids]
        for item_id, var in items:
            if item_id in selected_ids:
                var.set(True)

    def edit_selected_item(self):
        selection = self.ticket_types_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an item to edit.")
            return

        index = selection[0]
        self.ticket_type_id = self.ticket_types[index][0]
        self.load_ticket_type_data()

    def delete_selected_item(self):
        selection = self.ticket_types_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an item to delete.")
            return

        index = selection[0]
        ticket_type_id = self.ticket_types[index][0]
        cursor = self.db_conn.cursor()
        cursor.execute('DELETE FROM ticket_types WHERE id = ?', (ticket_type_id,))
        cursor.execute('DELETE FROM ticket_type_garments WHERE ticket_type_id = ?', (ticket_type_id,))
        cursor.execute('DELETE FROM ticket_type_colors WHERE ticket_type_id = ?', (ticket_type_id,))
        cursor.execute('DELETE FROM ticket_type_patterns WHERE ticket_type_id = ?', (ticket_type_id,))
        cursor.execute('DELETE FROM ticket_type_upcharges WHERE ticket_type_id = ?', (ticket_type_id,))
        cursor.execute('DELETE FROM ticket_type_coupons_discounts WHERE ticket_type_id = ?', (ticket_type_id,))
        cursor.execute('DELETE FROM ticket_type_textures WHERE ticket_type_id = ?', (ticket_type_id,))
        self.db_conn.commit()
        self.refresh_ticket_types_list()

def create_db_connection():
    conn = sqlite3.connect('pos_system.db')
    return conn

if __name__ == "__main__":
    db_conn = create_db_connection()

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = TicketTypeWindow(root, db_conn)
    app.mainloop()
    db_conn.close()