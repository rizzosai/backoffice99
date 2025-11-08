@app.route('/api/my-ip', methods=['GET'])
def get_my_ip():
    try:
        ip_response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_response.raise_for_status()
        return jsonify(ip_response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import os
from flask import Flask, request, jsonify, redirect
import requests
from dotenv import load_dotenv
from flask_cors import CORS
import requests

print("Render public IP:", requests.get('https://api.ipify.org').text)

load_dotenv()

app = Flask(__name__)
# Redirect root URL to the main back office
@app.route('/')
def root():
    return redirect('https://backoffice21.onrender.com/', code=302)
CORS(app)  # Allow all origins by default; restrict in production if needed

# Route to get the public IP address of the backend server
@app.route('/api/my-ip', methods=['GET'])
def get_my_ip():
    try:
        ip_response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_response.raise_for_status()
        return jsonify(ip_response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

NAMECHEAP_API_USER = os.getenv('NAMECHEAP_API_USER')
NAMECHEAP_API_KEY = os.getenv('NAMECHEAP_API_KEY')
NAMECHEAP_USERNAME = os.getenv('NAMECHEAP_USERNAME')
NAMECHEAP_CLIENT_IP = os.getenv('NAMECHEAP_CLIENT_IP')  # Must be whitelisted in Namecheap panel

@app.route('/api/claim-domain', methods=['POST'])
def claim_domain():
    data = request.get_json()
    domain = data.get('domain')
    email = data.get('email')
    if not domain or not email:
        return jsonify({'error': 'Missing domain or email'}), 400

    # Example: Check domain availability (Namecheap API)
    import sys
    api_url = 'https://api.namecheap.com/xml.response'
    params = {
        'ApiUser': NAMECHEAP_API_USER,
        'ApiKey': NAMECHEAP_API_KEY,
        'UserName': NAMECHEAP_USERNAME,
        'ClientIp': NAMECHEAP_CLIENT_IP,
        'Command': 'namecheap.domains.check',
        'DomainList': domain
    }

    resp = requests.get(api_url, params=params)
    print('Namecheap API status:', resp.status_code)
    print('Namecheap API response:', resp.text)
    if resp.status_code != 200 or '<Available>true</Available>' not in resp.text:
        return jsonify({'error': 'Domain not available or Namecheap error', 'details': resp.text}), 400
    # TODO: Register domain (see Namecheap API docs for full registration call)
    # ...
    # For demo, just return success
    return jsonify({'success': True, 'message': 'Domain is available and can be registered.'})

if __name__ == '__main__':
    app.run(debug=True)
