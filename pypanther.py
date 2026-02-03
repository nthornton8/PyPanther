from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import time
import requests
import socket
import os
from qrcode import QRCode
from api import get_chatbot_response  # Import the function
from api import pypanther
from data.api_key import API_KEY  

app = Flask(__name__)
CORS(app)

# Define the model you're using — you can change this later dynamically
MODEL = "aics"  # or aimusic, aianthropology, etc.

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data.get("message", "")
    
    # Get AI-generated response using the API
    reply = pypanther(MODEL, API_KEY, message)
    
    return jsonify({"answer": reply})

if __name__ == '__main__':
    app.run(port=5000)
