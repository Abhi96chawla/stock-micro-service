from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import bcrypt
import os

app = Flask(__name__)
CORS(app)

app.secret_key = "24"

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users1 (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    address TEXT NOT NULL,
                    postal_code VARCHAR(20) NOT NULL
                )
            ''')
            connection.commit()
        except Error as e:
            print(f"Error creating table: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    postal_code = data.get('postalCode')
    
    if not all([first_name, last_name, email, password, address, postal_code]):
        return jsonify({"message": "All fields are required"}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users1 (first_name, last_name, email, password, address, postal_code)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, email, hashed_password, address, postal_code))
            connection.commit()
            return jsonify({"message": "User created successfully"}), 201
        except Error as e:
            return jsonify({"message": f"Error creating user: {str(e)}"}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return jsonify({"message": "Unable to connect to the database"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users1 WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user'] = user['first_name']  # Store username in session
                return jsonify({"message": "Login successful", "user": user['first_name'], "redirect": True}), 200
            else:
                return jsonify({"message": "Invalid email or password"}), 401
        except Error as e:
            return jsonify({"message": f"Error during login: {str(e)}"}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return jsonify({"message": "Unable to connect to the database"}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logout successful"}), 200

@app.route('/api/welcome', methods=['GET'])
def welcome():
    if 'user' in session:
        return jsonify({"message": f"Welcome {session['user']}!"}), 200
    else:
        return jsonify({"message": "Not authorized"}), 403

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
