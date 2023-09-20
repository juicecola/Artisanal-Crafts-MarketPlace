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
        'name': 'giraffe',
        'price': 99.99,
        'category': 'Category 1',
        'image': 'uploads/giraffe.jpg',
        'details': 'A wooden curve of giraffe',
        'price_id': 'price_id_1'
    },
    {
        'name': 'basket',
        'price': 59.99,
        'category': 'Category 2',
        'image': 'uploads/basket.jpg',
        'details': 'A wood and coconut shell jewelry-box',
        'price_id': 'price_id_2'
    },
    {
        'name': 'viking helmet',
        'price': 115.50,
        'category': 'Category 3',
        'image': 'uploads/viking.jpg',
        'details': 'A Viking helmet for costume parties',
        'price_id': 'price_id_3'
    },
    {
        'name': 'treasure box',
        'price': 76.57,
        'category': 'Category 4',
        'image': 'uploads/homedecor.jpg',
        'details': 'A treasure box from the Maldives',
        'price_id': 'price_id_4'
    },
    {
        'name': 'art-deco',
        'price': 50.50,
        'category': 'Category 5',
        'image': 'uploads/art-deco.jpg',
        'details': 'An art decoration to hang on the wall',
        'price_id': 'price_id_5'
    },
    {
        'name': 'otomi-embroided-tote-bag',
        'price': 65.50,
        'category': 'Category 6',
        'image': 'uploads/otomi-embroided-tote-bag.jpg',
        'details': 'A very stylish hang bag mad with love',
        'price_id': 'price_id_6'
    },
    {
        'name': 'painting',
        'price': 30.00,
        'category': 'Category 7',
        'image': 'uploads/painting.jpg',
        'details': 'A stunning wall hanging from Morocco',
        'price_id': 'price_id_7'
    },
    {
        'name': 'sculpture',
        'price': 200.00,
        'category': 'Category 8',
        'image': 'uploads/sculpture.jpg',
        'details': 'A life size sculpture of a warrior in Ottoman',
        'price_id': 'price_id_8'
    },
    {
        'name': 'wall-hanging',
        'price': 40.50,
        'category': 'Category 9',
        'image': 'uploads/wall-hanging.jpg',
        'details': 'A wall hanging of a sunflower',
        'price_id': 'price_id_9'
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

