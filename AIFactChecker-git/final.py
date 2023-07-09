import sys
sys.path.insert(1,'/home/ubuntu')

from flask import Flask, request
from model import runModel
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/veritas')
def veritas():
    args = request.args
    output = runModel(args.get('news'))
    if 'fake' in output.lower():
        return 'fake'
    return 'real'

if __name__ == '__main__':
   app.run(host='0.0.0.0')
