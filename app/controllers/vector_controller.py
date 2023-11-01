from app import app
from flask import jsonify
from flask import request, jsonify
from werkzeug.utils import secure_filename
from app.services.vectore_service import allowed_file, create_vector

import re
import os

@app.route('/api/vector', methods=['GET'])
def vector_endpoint():
    # Xử lý logic cho endpoint /vector ở đây
    return jsonify({'message': 'This is the vector endpoint'}), 200

@app.route('/api/vector/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        filename = re.sub(r'[^\w.-]', '_', filename)

        filename = re.sub(r'__+', '_', filename)

        filename = filename.strip()

        filename = filename.lower()
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/vector', methods=['POST'])
def generate_vector():
    try:
        create_vector()
        return jsonify({'message': 'Generate successfully'}), 200
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500