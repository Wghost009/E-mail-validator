import os
import requests  # <-- Make sure this is imported at the top!
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. Automatically fetch the massive community list of thousands of burner domains
print("Fetching live disposable domain blocklist...")
try:
    blocklist_url = "https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/master/disposable_email_blocklist.conf"
    response = requests.get(blocklist_url, timeout=5)
    
    # Split the text file by line breaks and convert to a set for instant O(1) lookups
    DISPOSABLE_DOMAINS = set(response.text.splitlines())
    print(f"Successfully loaded {len(DISPOSABLE_DOMAINS)} burner domains!")
except Exception as e:
    print(f"Failed to fetch live list ({e}). Using local fallback.")
    # Safe fallback list just in case your laptop loses internet connection
    DISPOSABLE_DOMAINS = {"mailinator.com", "10minutemail.com", "yopmail.com", "tempmail.com"}

# 2. Your validation endpoint logic
@app.route('/api/v1/validate', methods=['GET'])
def validate_email():
    email = request.args.get('email', '').strip().lower()
    
    if not email or '@' not in email:
        return jsonify({
            "valid": False,
            "reason": "Invalid email structure provided"
        }), 400

    # Extract just the domain part (everything after the @)
    domain = email.split('@')[-1]

    # Check if the domain exists in our massive fetched set
    if domain in DISPOSABLE_DOMAINS:
        return jsonify({
            "email": email,
            "is_disposable": True,
            "reason": "Disposable / Burner email provider detected",
            "valid": False
        }), 200
    
    return jsonify({
        "email": email,
        "is_disposable": False,
        "reason": "Valid domain layout",
        "valid": True
    }), 200

@app.route('/ping', methods=['GET'])
def ping():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
