import sqlite3

# Define the Item class
class Item:
    def __init__(self, name, price, category, image, details, price_id):
        self.name = name
        self.price = price
        self.category = category
        self.image = image
        self.details = details
        self.price_id = price_id

# Create a list of items
items = [
    Item(
        name="giraffe",
        price=99.99,
        category="Category 1",
        image="/home/munyi/Downloads/giraffe.jpg",
        details="A wooden curve of giraffe",
        price_id="price_id_1"
    ),
    Item(
        name="jewelry-box",
        price=59.99,
        category="Category 2",
        image="/home/munyi/Downloads/wood-and-cocont-shell-jewelry-box.jpg",
        details="A wood and coconut shell jewelry-box",
        price_id="price_id_2"
    ),
    Item(
        name="viking helmet",
        price=115.50,
        category="Category 3",
        image="/home/munyi/Downloads/otomi-embroided-tote-bag.jpg",
        details="an embroided tote bag",
        price_id="price_id_3"
    ),
    Item(
        name="treasure box",
        price=76.57,
        category="Category 4",
        image="/home/munyi/Downloads/homedecor.jpg",
        details="a treasure box from Maldives",
        price_id="price_id_4"
    )
]

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("items.db")

# Create a cursor
cursor = conn.cursor()

# Create a table for items if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        category TEXT,
        image TEXT,
        details TEXT,
        price_id TEXT
    )
''')

# Insert items into the database
for item in items:
    cursor.execute('''
        INSERT INTO items (name, price, category, image, details, price_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (item.name, item.price, item.category, item.image, item.details, item.price_id))

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("Items inserted into the database successfully.")

