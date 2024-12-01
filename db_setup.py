import sqlite3

DATABASE = 'menu.db'

def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            accountId INTEGER PRIMARY KEY, 
            first_name TEXT, 
            last_name TEXT, 
            last_ordered_meal TEXT
        )
    ''')
    conn.commit()

    # Create pricing table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pricing (
            category TEXT,
            item TEXT,
            size TEXT,
            price REAL
        )
    ''')
    conn.commit()

    # Insert fake pricing data
    cursor.executemany('''
        INSERT OR IGNORE INTO pricing (category, item, size, price) VALUES (?, ?, ?, ?)
    ''', [
        ("main", "BIGMAC", None, 5.99),
        ("main", "QUARTER", None, 6.49),
        ("main", "CHICKEN", None, 5.49),
        ("main", "NUGGET", None, 4.99),
        ("main", "FISH", None, 5.99),
        ("side", "FRY", "S", 1.99),
        ("side", "FRY", "M", 2.49),
        ("side", "FRY", "L", 2.99),
        ("side", "POUTINE", "S", 2.99),
        ("side", "POUTINE", "M", 3.49),
        ("side", "POUTINE", "L", 3.99),
        ("drink", "COKE", "S", 1.49),
        ("drink", "COKE", "M", 1.99),
        ("drink", "COKE", "L", 2.49),
        ("drink", "SPRITE", "S", 1.49),
        ("drink", "SPRITE", "M", 1.99),
        ("drink", "SPRITE", "L", 2.49),
        ("drink", "WATER", "S", 0.99),
        ("drink", "WATER", "M", 1.49),
        ("drink", "WATER", "L", 1.99),
        ("drink", "ICEDT", "S", 1.49),
        ("drink", "ICEDT", "M", 1.99),
        ("drink", "ICEDT", "L", 2.49),
    ])
    conn.commit()
    conn.close()