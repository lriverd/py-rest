import logging.config
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from database import AmandaMessages
import time
import os

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

@app.route('/')
def hello_world():
  return os.environ.get('MONGO_URI')

@app.route('/status', methods=['GET'])
def get_status():
	output = {'Status': 'Ok'}
	return jsonify({'result': output})

@app.route('/customerorder-rpa', methods=['POST'])
def add_order_rpa():
	result = 'Succcess'
	detail = '65466868498465'
	return jsonify({'result': result, 'detail': detail})

@app.route('/customerorder', methods=['POST'])
def add_order():
	result = ''
	detail = ''
	try:
		mongo = PyMongo(app)
		order = mongo.db.orders
		header = request.json['Header']
		msge = request.json['Message']
		order_id = order.insert({'Header': header, 'Message': msge})
		new_order = order.find_one({'_id': order_id})
		output = {'Header': new_order['Header']}

		if output != '':
			detail = str(order_id)
			result = 'Succcess'
	except Exception as e:
		result = 'Error'
		detail = str(e)
	finally:
		return jsonify({'result': result, 'detail': detail})

@app.route('/customerorder2', methods=['POST'])
def add_order2():
	result = ''
	detail = ''
	try:
		client = MongoClient(os.environ.get('MONGO_URI'))
		order = client.test[str('orders')]
		header = request.json['Header']
		msge = request.json['Message']
		order_id = order.insert_one({'Header': header, 'Message': msge}).inserted_id
		new_order = order.find_one({'_id': order_id})
		output = {'Header': new_order['Header']}

		if output != '':
			result = 'Succcess'
	except Exception as e:
		result = 'Error'
		detail = str(e)
	finally:
		return jsonify({'result': result, 'detail': detail})

@app.route('/test2', methods=['GET'])
def add_test2():
	conversations = AmandaMessages()

	#conversations.set('123123',{'context.guia_despacho': False})
	conversations.push('123123123', {'messages': (str(time.time()), 'Hola ')})
	return 'Ok2'

if __name__ == '__main__':
	app.run(debug=True)
