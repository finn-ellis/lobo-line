from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from rag import run_query

app = Flask(__name__, static_folder='react-app/build/static', template_folder='react-app/build')
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/query', methods=['POST'])
def query():
    prompt = request.json.get('prompt')
    result = run_query(prompt)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True) 