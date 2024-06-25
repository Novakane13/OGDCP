import sqlite3

def create_db_connection(db_path='pos_system.db'):
    conn = sqlite3.connect(db_path)
    return conn

def initialize_db():
    conn = create_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            notes TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            ticket_number TEXT NOT NULL,
            rack TEXT,
            pieces INTEGER,
            total REAL,
            status TEXT,
            type TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ticket_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            garment_id INTEGER NOT NULL,
            variant_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id),
            FOREIGN KEY (garment_id) REFERENCES garments(id),
            FOREIGN KEY (variant_id) REFERENCES variations(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hex_value TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS garments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS variations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            garment_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (garment_id) REFERENCES garments(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS garment_prices (
            garment_id INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (garment_id) REFERENCES garments(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS variation_prices (
            variation_id INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (variation_id) REFERENCES variations(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ticket_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ticket_type_garments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_type_id INTEGER NOT NULL,
            garment_id INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (ticket_type_id) REFERENCES ticket_types(id),
            FOREIGN KEY (garment_id) REFERENCES garments(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupons_discounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            image TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS upcharges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ticket_type_upcharges (
            ticket_type_id INTEGER NOT NULL,
            upcharge_id INTEGER NOT NULL,
            FOREIGN KEY (ticket_type_id) REFERENCES ticket_types(id),
            FOREIGN KEY (upcharge_id) REFERENCES upcharges(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS textures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ticket_type_textures (
            ticket_type_id INTEGER NOT NULL,
            texture_id INTEGER NOT NULL,
            FOREIGN KEY (ticket_type_id) REFERENCES ticket_types(id),
            FOREIGN KEY (texture_id) REFERENCES textures(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quick_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            due_date TEXT NOT NULL,
            overall_notes TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quick_ticket_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quick_ticket_id INTEGER NOT NULL,
            ticket_type TEXT NOT NULL,
            pieces INTEGER NOT NULL,
            notes TEXT,
            FOREIGN KEY (quick_ticket_id) REFERENCES quick_tickets(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
