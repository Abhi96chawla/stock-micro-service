from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model for inventory items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

# Add new item
@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']
    new_item = Item(name=name, quantity=int(quantity), price=float(price))
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

# Update item
@app.route('/update/<int:id>', methods=['POST'])
def update_item(id):
    item = Item.query.get_or_404(id)
    item.name = request.form['name']
    item.quantity = request.form['quantity']
    item.price = request.form['price']
    db.session.commit()
    return redirect(url_for('index'))

# Delete item
@app.route('/delete/<int:id>')
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
