from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.rag import run_query
import os

app = Flask(__name__, static_folder='frontend/build/static', template_folder='frontend/build')
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/prompt', methods=['POST'])
def prompt():
    prompt_text = request.json.get('prompt').strip()
    if not prompt_text or prompt_text == "":
        return jsonify({'answer': 'You cannot submit an empty prompt.'})
    session_id = request.json.get('session_id')
    print(f"Received prompt: {prompt_text} with session_id: {session_id}")

    # Run the query with the existing or new session_id
    answer, id = run_query(prompt_text, session_id)

    return jsonify({'answer': answer, 'session_id': id})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))