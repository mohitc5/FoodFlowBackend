from flask import Flask, render_template, url_for, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db_setup import create_database
from utils import calculate_price, get_items_from_db
import sqlite3
from db_setup import DATABASE
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     content = db.Column(db.String(200),nullable = False)
#     completed = db.Column(db.Integer, default = 0)
#     date_created = db.Column(db.DateTime, default = datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id

# @app.cli.command('create-db')
# def create_db():
#     """Create the database tables."""
#     db.create_all()
#     print("Database tables created.")

# @app.route('/', methods=['POST','GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Todo(content = task_content)
        
#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Issue adding task'
#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks = tasks)

# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)
    
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'problem deleting task'

# @app.route('/update/<int:id>', methods =['POST','GET'])
# def update(id):
#     task = Todo.query.get_or_404(id)
#     if request.method == 'POST':
#         task.content = request.form['content']  
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Issue updating task'
#     else:
#         return render_template('update.html', task = task)
    
# for react https://www.youtube.com/watch?v=7LNl2JlZKHA

@app.route('/calculate_price', methods=['POST'])
def calculate_price_endpoint():
    order = request.json
    total_price = calculate_price(order)
    order["total_price"] = round(total_price, 2)
    return jsonify(order)

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    account_id = data.get("accountId")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    
    if not (account_id and first_name and last_name):
        return jsonify({"error": "Missing account details"}), 400
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO accounts (accountId, first_name, last_name, last_ordered_meal)
            VALUES (?, ?, ?, NULL)
        ''', (account_id, first_name, last_name))
        conn.commit()
        return jsonify({"message": "Account created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Account ID already exists"}), 400
    finally:
        conn.close()

    # @app.route('/send_to_frontend', methods=['POST'])
    # def send_to_frontend():
    #     import requests
    #     frontend_url = "http://localhost:3000/api/order"  # Replace with the actual frontend URL
    #     order = request.json
    #     response = requests.post(frontend_url, json=order)
    #     return jsonify({"status": response.status_code, "message": response.text})
@app.route('/get_account/<int:account_id>', methods=['GET'])
def get_account(account_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE accountId = ?', (account_id,))
    account = cursor.fetchone()
    conn.close()

    if account:
        
        last_ordered_meal = json.loads(account[3]) if account[3] else None
        
        return jsonify({
            "accountId": account[0],
            "first_name": account[1],
            "last_name": account[2],
            "last_ordered_meal": last_ordered_meal
        })
    else:
        return jsonify({"error": "Account not found"}), 404
    
    
@app.route('/update_last_ordered_meal', methods=['POST'])
def update_last_ordered_meal():
    data = request.json
    account_id = data.get("accountId")
    last_ordered_meal = data.get("last_ordered_meal")  # Full JSON order

    if not (account_id and last_ordered_meal):
        return jsonify({"error": "Missing account ID or last ordered meal"}), 400


    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    last_ordered_meal_json = json.dumps(last_ordered_meal)
    try:
        cursor.execute('''
            UPDATE accounts
            SET last_ordered_meal = ?
            WHERE accountId = ?
        ''', (last_ordered_meal_json, account_id))
        conn.commit()
    finally:
        conn.close()

    if cursor.rowcount > 0:
        return jsonify({"message": "Last ordered meal updated successfully"})
    else:
        return jsonify({"error": "Account not found"}), 404
    
@app.route('/process_transcription', methods=['POST'])
def process_transcription():
    data = request.json
    transcription = data.get("user_input")
    # Process transcription (e.g., log, analyze, or save)
    print("Received transcription:", transcription)
    return jsonify({"status": "success", "message": "Transcription processed"})

@app.route('/get_menu', methods=['GET'])
def get_menu():
    menu_items = get_items_from_db()
    if not menu_items:
        return "No menu items available", 404
    return jsonify(menu_items)
    
    
create_database()

if (__name__) == '__main__':
    app.run(debug = True)