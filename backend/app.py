
# --- CLEANED UP SINGLE VERSION BELOW ---
import os
import random
import string
import requests
from flask import Flask, send_from_directory, request, jsonify, redirect
from flask_cors import CORS
from dotenv import load_dotenv

print("Render public IP:", requests.get('https://api.ipify.org').text)

load_dotenv()

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

# Utility to generate a random username
def generate_username(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Utility to create an affiliate link with your username
def create_affiliate_link(base_url, username):
    return f"{base_url}?ref={username}"

# API endpoint to generate usernames and affiliate links
@app.route('/api/generate-demo-users', methods=['POST'])
def generate_demo_users():
    data = request.get_json()
    count = data.get('count', 10)
    base_url = data.get('base_url', 'https://rizzosai.com/affiliate')
    your_username = data.get('your_username', 'yourusername')
    users = []
    for _ in range(count):
        uname = generate_username()
        users.append({
            'username': uname,
            'affiliate_link': create_affiliate_link(base_url, your_username)
        })
    return jsonify({'users': users})

# Route to get the public IP address of the backend server
@app.route('/api/my-ip', methods=['GET'])
def get_my_ip():
    try:
        ip_response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_response.raise_for_status()
        return jsonify(ip_response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Namecheap domain claim endpoint
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
    api_url = 'https://api.namecheap.com/xml.response'
    params = {
        'ApiUser': NAMECHEAP_API_USER,
        'ApiKey': NAMECHEAP_API_KEY,
        'UserName': NAMECHEAP_USERNAME,
        'ClientIp': NAMECHEAP_CLIENT_IP,
        'Command': 'namecheap.domains.check',
        'DomainList': domain
    # In-memory storage for live feed events (for demo; use a database in production)
    live_events = [
        {"type": "signup", "message": "User topgun1 signed up.", "time": "1 min ago"},
        {"type": "payment", "message": "User rizzking made a payment.", "time": "2 min ago"},
        {"type": "signup", "message": "User affiliateguru signed up.", "time": "5 min ago"},
        {"type": "payment", "message": "User hustler made a payment.", "time": "10 min ago"},
    ]

    # Endpoint to receive email/payment form submissions
    from datetime import datetime
    @app.route('/api/submit-user', methods=['POST'])
    def submit_user():
        data = request.get_json()
        email = data.get('email')
        payment = data.get('payment')
        if not email or not payment:
            return jsonify({'error': 'Missing email or payment info'}), 400
        # Add to live feed (newest first)
        event = {
            'type': 'signup',
            'message': f"New signup: {email} (Payment: {payment})",
            'time': datetime.now().strftime('%H:%M')
        }
        live_events.insert(0, event)
        # Limit to last 20 events
        if len(live_events) > 20:
            live_events.pop()
        return jsonify({'success': True})
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
    app.run(debug=True)

