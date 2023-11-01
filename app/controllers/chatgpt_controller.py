from app import app
from flask import jsonify, request
from app.services.chatgpt_service import chat_default, chat

@app.route('/', methods=['GET'])
def endpoint():
     return jsonify({'data': 'Hello world 💫'})

@app.route('/api/chatgpt/chat-default', methods=['POST'])
def chat_default_endpoint():
    data = request.get_json()
    query = data.get('query')
    if query:
        result = chat_default(query)
        return jsonify({'answer': result})
    else:
        return jsonify({'error': 'Invalid request'})
    
@app.route('/api/chatgpt/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.get_json()
        query = data.get('query')
        if query:
            result = chat(query)
            return jsonify({'answer': result})
        else:
            return jsonify({'error': 'Invalid request'})
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500