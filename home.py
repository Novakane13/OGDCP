import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from customer_account import CustomerAccountWindow
from customer_search import CustomerSearchWindow
from ticket_type import TicketTypeWindow  # Correct import
from color_list_creation import ColorListCreationWindow
from garment_list_creation import GarmentListCreationWindow
from pattern_list_creation import PatternListCreationWindow
from coupons_and_discounts import CouponsAndDiscountsCreationWindow
from upcharges_list_creation import UpchargesListCreationWindow
from textures_list_creation import TexturesListCreationWindow
from initialize_db import create_db_connection  # Correct import

# Main HomeWindow Class
class HomeWindow(tk.Tk):
    def __init__(self, db_conn):
        super().__init__()
        self.db_conn = db_conn
        self.title("Ogden's Dry Clean Program")
        self.geometry("2000x1200")  # Set a default size for the window
        self.create_menu()
        self.create_widgets()
    
    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Upload Image", command=self.upload_image)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def create_widgets(self):
        # Frame for buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        button_data = [
            ("Next Customer", self.open_search_window),
            ("Ticket Type Creation", self.open_ticket_type_creation_window),
            ("Delivery Route Creation", self.open_delivery_route_creation),
            ("Garment Creation", self.open_garment_creation),
            ("Design Specials", self.open_design_specials),
            ("Color List Creation", self.open_color_list_creation_window),
            ("Pattern List Creation", self.open_pattern_list_creation_window),
            ("Coupons and Discounts Creation", self.open_coupons_discounts_creation_window),
            ("Upcharges List Creation", self.open_upcharges_creation_window),
            ("Textures List Creation", self.open_textures_creation_window)
        ]

        for text, command in button_data:
            button = ttk.Button(self.buttons_frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame for the image
        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(side=tk.TOP, pady=10)

    def open_search_window(self):
        CustomerSearchWindow(self, self.db_conn)

    def open_ticket_type_creation_window(self):
        TicketTypeWindow(self, self.db_conn)

    def open_delivery_route_creation(self):
        messagebox.showinfo("Delivery Route Creation", "Delivery Route Creation functionality not yet implemented.")

    def open_garment_creation(self):
        GarmentListCreationWindow(self, self.db_conn)

    def open_design_specials(self):
        messagebox.showinfo("Design Specials", "Design Specials functionality not yet implemented.")

    def open_color_list_creation_window(self):
        ColorListCreationWindow(self, self.db_conn)

    def open_pattern_list_creation_window(self):
        PatternListCreationWindow(self, self.db_conn)

    def open_coupons_discounts_creation_window(self):
        CouponsAndDiscountsCreationWindow(self, self.db_conn)

    def open_upcharges_creation_window(self):
        UpchargesListCreationWindow(self, self.db_conn)

    def open_textures_creation_window(self):
        TexturesListCreationWindow(self, self.db_conn)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.display_image(file_path)

    def display_image(self, file_path):
        image = Image.open(file_path)
        image = image.resize((self.image_frame.winfo_width(), self.image_frame.winfo_height()), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)
        self.image_label.image = self.photo

if __name__ == "__main__":
    # Create or connect to your database
    db_conn = create_db_connection()

    home_app = HomeWindow(db_conn)
    home_app.mainloop()
