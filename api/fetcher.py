# server.py
# This server is now a single, combined application that serves both the
# frontend (index.html) and the backend API endpoint.

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

# Initialize the Flask application, telling it where to find static files.
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

@app.route('/')
def index():
    """
    Serve the main index.html file from the 'static' directory.
    """
    return send_from_directory('static', 'index.html')

@app.route('/fetch-url', methods=['POST'])
def fetch_url():
    """
    API endpoint to fetch the content of a given URL.
    """
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL not provided in the request body'}), 400

        url_to_fetch = data['url']
        response = requests.get(url_to_fetch, timeout=10)
        response.raise_for_status()
        return jsonify({'content': response.text})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch URL: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

# This block is for local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
