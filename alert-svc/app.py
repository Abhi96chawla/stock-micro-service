import os
import json
import time
import threading
import yfinance as yf
from flask import Flask, request, jsonify, render_template
from google.cloud import pubsub_v1

# Set the path to your Google Cloud service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"bubbly-mantis.json"

app = Flask(__name__)

# Initialize Google Cloud Pub/Sub variables
project_id = "python-project-cluster"
topic_id = "my-topic"
subscription_id = "my-sub"

# Initialize Pub/Sub publisher and subscriber clients
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Route to render the form and handle alert submissions
@app.route('/set-alert', methods=['GET', 'POST'])
def stock_alert():
    if request.method == 'POST':
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

        # Publish alert data to Pub/Sub topic
        alert_data = {
            'email': email,
            'stock': stock_symbol.upper(),
            'threshold': price_threshold
        }

        # Log the alert data being published
        print(f"Publishing message: {alert_data}")

        # Publish the alert data as a JSON string to the Pub/Sub topic
        future = publisher.publish(topic_path, json.dumps(alert_data).encode("utf-8"))
        future.result()  # Wait for publishing to complete

        return jsonify({'message': f'Stock alert for {stock_symbol} set at price {price_threshold} successfully!'})

    # Render the `salert.html` template when the request is a GET
    return render_template('salert.html')

# Function to process alerts from Pub/Sub subscription
def process_alert(message):
    # Print the raw message data to check if it's empty or not valid
    print(f"Received message data: {message.data}")

    try:
        # Try decoding the message data
        alert = json.loads(message.data)
        stock_symbol = alert['stock']
        threshold = alert['threshold']
        email = alert['email']

        try:
            # Fetch current stock price
            stock_data = yf.Ticker(stock_symbol)
            stock_price = stock_data.history(period="1d")['Close'][0]

            # Log stock data and check if current price meets or exceeds threshold
            print(f"Stock: {stock_symbol}, Price: {stock_price}, Threshold: {threshold}")

            if stock_price >= threshold:
                send_notification(email, stock_symbol, stock_price)
        except Exception as e:
            print(f"Error processing alert for {stock_symbol}: {str(e)}")
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode message: {message.data} with error: {str(e)}")

    message.ack()  # Acknowledge the message after processing

# Dummy function to simulate sending a notification
def send_notification(email, stock_symbol, stock_price):
    print(f"Notification sent to {email}: {stock_symbol} has reached ${stock_price}")

# Start Pub/Sub subscription listener in a separate thread
def start_pubsub_subscriber():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_alert)
    print("Listening for messages on {}...".format(subscription_path))
    try:
        streaming_pull_future.result()
    except Exception as e:
        streaming_pull_future.cancel()
        print(f"Listening for messages on {subscription_path} threw an exception: {e}")

# Start the Flask app and Pub/Sub subscriber thread
if __name__ == '__main__':
    # Start the subscriber thread to listen to incoming messages
    thread = threading.Thread(target=start_pubsub_subscriber)
    thread.daemon = True
    thread.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=5003, debug=True)
