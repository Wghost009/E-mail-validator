from flask import Flask, jsonify, request
import os
from flask import Flask, jsonify, request
import re # Make sure this is at the top of your file with your other imports!

if __name__ == '__main__':
    # Pull the port from the cloud environment, or use 5000 as a local fallback
    port = int(os.environ.get("PORT", 5000))
    
    # Run the app globally bound to 0.0.0.0 so the cloud gateway can reach it
    app.run(host="0.0.0.0", port=port)
app = Flask(__name__)

# Regular expression pattern for basic email syntax validation
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@app.route('/api/v1/validate', methods=['GET'])
def validate_email():

# Blocklist of common disposable / burner email domains
DISPOSABLE_DOMAINS = {
    "mailinator.com", 
    "10minutemail.com", 
    "yopmail.com", 
    "tempmail.com", 
    "sharklasers.com"
}

# Blocklist of generic corporate roles
ROLE_PREFIXES = {"admin", "support", "info", "sales", "contact", "jobs"}

@app.route('/api/v1/validate', methods=['GET'])
def validate_email():
    # Grab the email parameter from the URL (e.g., ?email=test@domain.com)
    email = request.args.get('email', '').strip().lower()
    
    # If no email was provided in the request
    if not email:
        return jsonify({"error": "Missing 'email' parameter in request"}), 400
        
    # 1. Syntax Check
    if not re.match(EMAIL_REGEX, email):
        return jsonify({
            "email": email,
            "valid": False,
            "reason": "Invalid syntax format"
        }), 200

    # Split the email into local part (user) and domain part
    try:
        user_part, domain_part = email.split('@', 1)
    except ValueError:
        return jsonify({"email": email, "valid": False, "reason": "Malformed email"}), 200

    # 2. Disposable Domain Check
    if domain_part in DISPOSABLE_DOMAINS:
        return jsonify({
            "email": email,
            "valid": False,
            "is_disposable": True,
            "reason": "Disposable / Burner email provider detected"
        }), 200

    # 3. Role-based Account Check
    is_role_account = user_part in ROLE_PREFIXES

    # If it passes all checks, it's a valid, clean email address!
    return jsonify({
        "email": email,
        "valid": True,
        "domain": domain_part,
        "is_disposable": False,
        "is_role_account": is_role_account,
        "reason": "Email looks clean and authentic"
    }), 200

if __name__ == '__main__':
    app.run(port=5000)
