import os
from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Downloadable Cheap Traffic Guide
@app.route('/guides/download/cheap-traffic')
def download_cheap_traffic_guide():
    return send_from_directory('static/guides', 'cheap_traffic_guide.html', as_attachment=True)

# Downloadable Facebook Affiliate Guide
@app.route('/guides/download/facebook')
def download_facebook_affiliate_guide():
    return send_from_directory('static/guides', 'facebook_affiliate_guide.html', as_attachment=True)

# Downloadable Instagram Affiliate Guide
@app.route('/guides/download/instagram')
def download_instagram_affiliate_guide():
    return send_from_directory('static/guides', 'instagram_affiliate_guide.html', as_attachment=True)

# Downloadable Twitter Affiliate Guide
@app.route('/guides/download/twitter')
def download_twitter_affiliate_guide():
    return send_from_directory('static/guides', 'twitter_affiliate_guide.html', as_attachment=True)

# Downloadable TikTok Affiliate Guide
@app.route('/guides/download/tiktok')
def download_tiktok_affiliate_guide():
    return send_from_directory('static/guides', 'tiktok_affiliate_guide.html', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, request, jsonify, redirect, send_from_directory
import requests
from dotenv import load_dotenv
from flask_cors import CORS
import requests

print("Render public IP:", requests.get('https://api.ipify.org').text)

load_dotenv()

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)
# Redirect root URL to the main back office
@app.route('/guides/download/cheap-traffic')
def download_cheap_traffic_guide():
    return send_from_directory('static/guides', 'cheap_traffic_guide.html', as_attachment=True)
# Route to get the public IP address of the backend server
@app.route('/api/my-ip', methods=['GET'])
def get_my_ip():
    try:
        ip_response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_response.raise_for_status()
        return jsonify(ip_response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import os
from flask import Flask, request, jsonify, redirect, send_from_directory
import requests
from dotenv import load_dotenv
from flask_cors import CORS

print("Render public IP:", requests.get('https://api.ipify.org').text)

load_dotenv()

app = Flask(__name__)

# Downloadable cheap traffic guide
@app.route('/guides/download/cheap-traffic')
def download_cheap_traffic_guide():
    return send_from_directory('static/guides', 'cheap_traffic_guide.html', as_attachment=True)

# Downloadable Facebook Affiliate Guide
@app.route('/guides/download/facebook')
def download_facebook_affiliate_guide():
    return send_from_directory('static/guides', 'facebook_affiliate_guide.html', as_attachment=True)

# Downloadable TikTok Affiliate Guide
@app.route('/guides/download/tiktok')
def download_tiktok_affiliate_guide():
    return send_from_directory('static/guides', 'tiktok_affiliate_guide.html', as_attachment=True)

# Downloadable Instagram Affiliate Guide
@app.route('/guides/download/instagram')
def download_instagram_affiliate_guide():
    return send_from_directory('static/guides', 'instagram_affiliate_guide.html', as_attachment=True)

# Downloadable Twitter Affiliate Guide
@app.route('/guides/download/twitter')
def download_twitter_affiliate_guide():
    return send_from_directory('static/guides', 'twitter_affiliate_guide.html', as_attachment=True)

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

