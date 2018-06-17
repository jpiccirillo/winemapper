#!env/bin/python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World! This is the updated version of the application.'

if __name__ == "__main__":
	app.run(host='0.0.0.0', port="5000", debug = False)
