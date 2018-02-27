
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


@app.route('/customerorder', methods=['POST'])
def add_order():
	result = ''
	detail = ''
	try:
		order = mongo.db.orders
		header = request.json['Header']
		msge = request.json['Message']
		order_id = order.insert({'Header': header, 'Message': msge})
		new_order = order.find_one({'_id': order_id})
		output = {'Header': new_order['Header']}

		if output != '':
			result = 'Succcess'
	except Exception as e:
		result = 'Error'
		detail = str(e)
	finally:
		return jsonify({'result': result, 'detail': detail})


if __name__ == '__main__':
	app.run(debug=True)
