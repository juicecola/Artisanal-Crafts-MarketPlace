import os
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('artisan.db')
cursor = conn.cursor()

# Path to the directory containing the images
image_dir = 'static/uploads/'

# List all files in the image directory
image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

# Define a common price_id for all images
price_id = 'common_price_id'

# Create a list of items with correct image paths
items = [
    {
        'name': 'baskets',
        'price': 99.99,
        'category': 'Category 10',
        'image': 'uploads/baskets.jpg',
        'details': 'handmade from nepal',
        'price_id': 'price_id_10'  # Corrected 'price_id'
    },
    {
        'name': 'crotchet',
        'price': 30.00,
        'category': 'Category 11',
        'image': 'uploads/crotchet.jpg',
        'details': 'pure cotton',
        'price_id': 'price_id_11'  # Corrected 'price_id'
    }
    # Add more items here with correct image paths and details
]

# Insert each item into the database
for item in items:
    cursor.execute("INSERT INTO items (name, price, category, image, details, price_id) VALUES (?, ?, ?, ?, ?, ?)",
                   (item['name'], item['price'], item['category'], item['image'], item['details'], item['price_id']))

# Commit the changes and close the database connection
conn.commit()
conn.close()

# Print a message indicating successful insertion
print("Items inserted into the database successfully.")

