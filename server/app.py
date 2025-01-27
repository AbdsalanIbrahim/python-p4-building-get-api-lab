#!/usr/bin/env python3

import logging
from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    try:
        # Fetch all bakeries from the database and convert them to JSON
        all_bakeries = Bakery.query.all()
        return jsonify([bakery.to_dict() for bakery in all_bakeries])
    except Exception as e:
        app.logger.error(f"Error fetching bakeries: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    try:
        # Fetch a single bakery by ID and include its baked goods
        bakery = Bakery.query.get_or_404(id)
        return jsonify(bakery.to_dict(nested=True))
    except Exception as e:
        app.logger.error(f"Error fetching bakery by id {id}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    try:
        # Fetch all baked goods sorted by price in descending order
        baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
        return jsonify([baked_good.to_dict() for baked_good in baked_goods])
    except Exception as e:
        app.logger.error(f"Error fetching baked goods by price: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    try:
        # Fetch the single most expensive baked good
        most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
        return jsonify(most_expensive.to_dict())
    except Exception as e:
        app.logger.error(f"Error fetching most expensive baked good: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)
