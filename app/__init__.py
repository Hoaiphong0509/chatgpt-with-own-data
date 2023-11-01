from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/assets'

CORS(app)

from app.controllers.chatgpt_controller import *
from app.controllers.vector_controller import *