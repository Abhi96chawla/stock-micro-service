import os
import time
import threading
import json
import yfinance as yf
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# Store alerts in memory (use a database in production)
alerts = []

# Route to render the stock alert form and handle alert submissions
@app.route('/set-alert', methods=['GET', 'POST'])
def stock_alert():
    if request.method == 'POST':
        # Extract form data from JSON (coming from the frontend)
        data = request.json
        stock_symbol = data.get('stock')
        price_threshold = data.get('threshold')
        email = data.get('email')

        # Input validation
        if not stock_symbol or not price_threshold or not email:
            return jsonify({'message': 'All fields are required!'}), 400

        try:
            price_threshold = float(price_threshold)
        except ValueError:
            return jsonify({'message': 'Invalid price threshold!'}), 400

        # Add the alert to the list
        alerts.append({
            'email': email,
            'stock': stock_symbol.upper(),  # Convert stock symbols to uppercase
            'threshold': price_threshold
        })

        return jsonify({'message': f'Stock alert for {stock_symbol} set at price {price_threshold} successfully!'})

    # Render the stock alert form
    return render_template('salert.html')

# Function to check stock prices and send notifications
def check_stock_prices():
    while True:
        for alert in alerts:
            stock_symbol = alert['stock']
            threshold = alert['threshold']
            email = alert['email']

            try:
                # Fetch the current stock price using yfinance
                stock_data = yf.Ticker(stock_symbol)
                stock_price = stock_data.history(period="1d")['Close'][0]

                # Check if the current price crosses the threshold
                if stock_price >= threshold:
                    send_notification(email, stock_symbol, stock_price)
            except Exception as e:
                print(f"Error checking stock price for {stock_symbol}: {str(e)}")

        time.sleep(300)  # Check every 5 minutes

# Dummy function to simulate sending a notification
def send_notification(email, stock_symbol, stock_price):
    print(f"Notification sent to {email}: {stock_symbol} has reached ${stock_price}")

# Start background thread for stock price monitoring
def start_monitoring():
    thread = threading.Thread(target=check_stock_prices)
    thread.daemon = True
    thread.start()

# Start the Flask app and monitoring thread
if __name__ == '__main__':
    start_monitoring()
    app.run(host='0.0.0.0', port=5003, debug=True)
