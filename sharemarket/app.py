from flask import Flask, render_template, jsonify, request, send_file
import requests
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Replace with your Alpha Vantage API key
API_KEY = 'AR1DEA06D12FGNNA'

# Function to get stock data from the API
def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if 'Time Series (5min)' in data:
        time_series = data['Time Series (5min)']
        times = []
        prices = []
        for time, values in time_series.items():
            times.append(time)
            prices.append(float(values['1. open']))
        return {
            'symbol': symbol,
            'times': times[:20],  # Limit to last 20 data points
            'prices': prices[:20]  # Limit to last 20 data points
        }
    else:
        return {'error': 'Error fetching data'}

# Function to create chart
def create_chart(symbol, times, prices):
    plt.figure(figsize=(10, 6))
    plt.plot(times, prices)
    plt.title(f'{symbol} Stock Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return f'data:image/png;base64,{graph_url}'

# Flask route to serve the stocks HTML page
@app.route('/stocks', methods=['GET', 'POST'])
def stock_page():
    if request.method == 'POST':
        symbol = request.form['symbol']
        data = get_stock_data(symbol)
        if 'error' in data:
            return render_template('stocks.html', error=data['error'])
        chart_url = create_chart(data['symbol'], data['times'], data['prices'])
        return render_template('stocks.html', symbol=data['symbol'], chart_url=chart_url)
    return render_template('stocks.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)