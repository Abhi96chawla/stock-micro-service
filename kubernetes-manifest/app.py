from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import csv
from io import StringIO, BytesIO
from urllib.parse import quote_plus

app = Flask(__name__)

# Configure MySQL Database connection
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

db_password_encoded = quote_plus(DB_PASSWORD)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{db_password_encoded}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a stock model
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Route for the main page
@app.route('/')
def index():
    stocks = Stock.query.all()  # Fetch all stocks from the database
    return render_template('index.html', stocks=stocks)

# Search stock using Alpha Vantage API
@app.route('/search_stock', methods=['POST'])
def search_stock():
    stock_code = request.form['stock_code']
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')  # Set your Alpha Vantage API Key as an environment variable
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_code}&interval=5min&apikey={api_key}'

    response = requests.get(url)
    data = response.json()

    if 'Time Series (5min)' in data:
        latest_time = next(iter(data['Time Series (5min)']))
        latest_data = data['Time Series (5min)'][latest_time]
        stock_price = float(latest_data['1. open'])
        return jsonify({'symbol': stock_code, 'price': stock_price})
    
    return jsonify({}), 404

# Add stock to the checklist
@app.route('/add_stock', methods=['POST'])
def add_stock():
    stock_symbol = request.form['symbol']
    stock_name = request.form['name']
    stock_price = request.form['price']
    
    new_stock = Stock(name=stock_name, symbol=stock_symbol, price=stock_price)
    db.session.add(new_stock)
    db.session.commit()
    
    return redirect(url_for('index'))

# Delete stock from the checklist
@app.route('/delete_stock/<int:stock_id>', methods=['POST'])
def delete_stock(stock_id):
    stock = Stock.query.get_or_404(stock_id)
    db.session.delete(stock)
    db.session.commit()
    return redirect(url_for('index'))

# Download CSV file of the stock checklist

@app.route('/download_csv')
def download_csv():
    # Create a string buffer
    output = StringIO()
    writer = csv.writer(output)
    
    # Write the header
    writer.writerow(['ID', 'Name', 'Symbol', 'Price'])
    
    # Write the data
    stocks = Stock.query.all()
    for stock in stocks:
        writer.writerow([stock.id, stock.name, stock.symbol, stock.price])
    
    # Get the string value and encode it
    output_string = output.getvalue()
    
    # Create a bytes buffer
    bytes_output = BytesIO()
    bytes_output.write(output_string.encode('utf-8-sig'))  # utf-8-sig adds BOM for Excel compatibility
    bytes_output.seek(0)
    
    return send_file(
        bytes_output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='stock_checklist.csv'
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)
