
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')
def hello_world():
  return 'Application Up'

@app.route('/status', methods=['GET'])
def get_status():
	output = {'Status': 'Ok'}
	return jsonify({'result': output})


@app.route('/order', methods=['POST'])
def add_order():
	result = ''
	detail = ''
	try:
		order = mongo.db.orders
		tXML = request.json['tXML']
		# msge = request.json['Message']
		order_id = order.insert({'tXML': tXML})
		new_order = order.find_one({'_id': order_id})
		output = {'tXML': new_order['tXML']}

		if output != '':
			result = 'Succcess'
	except Exception as e:
		result = 'Error'
		detail = str(e)
	finally:
		return jsonify({'result': result, 'detail': detail})


if __name__ == '__main__':
	app.run()
