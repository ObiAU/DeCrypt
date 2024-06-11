from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from config import SESSION_KEY
from query_processor import Processor

app = Flask(__name__)
app.secret_key = SESSION_KEY
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_query', methods=['POST'])
def handle_query():
    return Processor.process_query()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    # app.run(debug = True)
