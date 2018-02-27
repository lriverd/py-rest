from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Servidor Up'

@app.route('/status', methods=['GET'])
def get_status():
	output = {'Status': 'Ok'}
	return jsonify({'result': output})

if __name__ == '__main__':
  app.run()
