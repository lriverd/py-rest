#import logging.config
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from database import AmandaMessages
import logging
import time
import sys
import os

#logging.config.fileConfig('logging.ini')
#logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info('Iniciando aplicacion')

app = Flask(__name__)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
#mongo = PyMongo(app)

@app.route('/')
def hello_world():
	output = {'Status': 'Flask Application Up'}
	return jsonify({'result': output})

@app.route('/status', methods=['GET'])
def get_status():
	logger.debug('Status correcto')
	logger.info('Llamada a status')
	output = {'Status': 'Ok'}
	return jsonify({'result': output})

@app.route('/customerorder-rpa', methods=['POST'])
def add_order_rpa():
	result = ''
	detail = ''
	try:
		order = mongo.db.orders_jueves
		#order = mongo.db.orders_rpa
		ord = request.json['Body']['clienteSubOrdenResponse']['orden']
		subOrd = request.json['Body']['clienteSubOrdenResponse']['subOrdenLista']
		lineas = request.json['Body']['clienteSubOrdenResponse']['lineas']
		ord['clienteCelularLimpio'] = limpiaNumero(ord['clienteCelular'])
		order_id = order.insert_one({'estado_conversacion':None, 'orden': ord, 'subOrdenLista': subOrd, 'lineas': lineas}).inserted_id
		new_order = order.find_one({'_id': order_id})
		output = {'orden': new_order['orden']}
		if output != '':
			detail = str(order_id)
			result = 'Succcess'
	except Exception as e:
		result = 'Error'
		detail = str(e)
	finally:
		return jsonify({'result': result, 'detail': detail})

@app.route('/customerorder', methods=['POST'])
def add_order():
	result = ''
	detail = ''
	try:
		#mongo = PyMongo(app)
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

@app.route('/orderjueves', methods=['POST'])
def add_order_jueves():
	result = ''
	detail = ''
	try:		
		order = mongo.db.orders_jueves
		ord = request.json['orden']
		subOrd = request.json['subOrdenLista']
		lineas = request.json['lineas']
		order_id = order.insert_one({'estado_conversacion':None, 'orden': ord, 'subOrdenLista': subOrd, 'lineas': lineas}).inserted_id
		new_order = order.find_one({'_id': order_id})
		output = {'orden': new_order['orden']}
		if output != '':
			detail = str(order_id)
			result = 'Succcess'
	except Exception as e:
		result = 'Error'
		detail = str(e)
	finally:
		return jsonify({'result': result, 'detail': detail})

def limpiaNumero(nro: str):
	numeros = "0123456789"
	resp = ""
	for n in nro:
		if n in numeros:
			resp += n
	resp = resp[-8:]
	resp = "569" + resp
	return resp

if __name__ == '__main__':
	app.run(debug=True)
	#if len(sys.argv) > 1:
	#	print(limpiaNumero(str(sys.argv[1])))
