import sqlite3
from db_setup import DATABASE

def calculate_price(order):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    total_price = 0.0

    # Calculate price for mains
    for main in order.get("main", []):
        cursor.execute("SELECT price FROM pricing WHERE category = 'main' AND item = ?", (main["item"],))
        main_price = cursor.fetchone()
        if main_price:
            total_price += main_price[0]
            if main["combo"]:
                total_price -= 1 


    # Calculate price for sides
    for side in order.get("side", []):
        cursor.execute("SELECT price FROM pricing WHERE category = 'side' AND item = ? AND size = ?", 
                       (side["item"], side["size"]))
        side_price = cursor.fetchone()
        if side_price:
            total_price += side_price[0]

    # Calculate price for drinks
    for drink in order.get("drink", []):
        cursor.execute("SELECT price FROM pricing WHERE category = 'drink' AND item = ? AND size = ?", 
                       (drink["item"], drink["size"]))
        drink_price = cursor.fetchone()
        if drink_price:
            total_price += drink_price[0]

    conn.close()
    return total_price

def get_items_from_db():
    """Fetch menu items from the database."""
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Execute the query to retrieve menu items
        cursor.execute('SELECT item, price FROM pricing')
        menu_items = cursor.fetchall()  # This retrieves a list of tuples (item, price)
        
        # Format the results into a list of dictionaries
        menu = [{"item": item, "price": price} for item, price in menu_items]
        
        # Close the connection
        conn.close()
        
        return menu
    except Exception as e:
        print(f"Error: {e}")
        return None