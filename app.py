from flask import Flask, request, jsonify
from webhooks import *
import os

app = Flask(__name__)

@app.route('/callback', methods=['POST'])
def handle_callback_request():
    # Ensure the request contains JSON data
    if request.is_json:
        try:
            callback_data = request.get_json()
            # Call the handle_callback function to process the data
            handle_callback(callback_data)
            return jsonify({"message": "Callback data processed successfully"}), 200
        except Exception as e:
            return jsonify({"error": "Error processing callback data", "details": str(e)}), 500
    else:
        return jsonify({"error": "Invalid request format"}, 400)

@app.route('/register_cbn_user', methods=['POST'])
def register_cbn_user_route():
    data = request.get_json()

    # Change data['planType'] to 'BASIC' if it is 'Free plan'
    if data['planType'] == 'Free plan':
        data['planType'] = 'BASIC'
        data['free_registration'] = True

    account_type = validate_account_type(data['planType'])
    if not account_type:
        return jsonify({'error': 'Invalid Account Plan'}), 400

    referee = validate_referral(data['referralCode'])
    if not referee:
        return jsonify({'error': 'Referral code given is invalid'}), 404

    user_by_phone = validate_user_by_phone(data['phone'])
    if user_by_phone:
        return jsonify({'error': 'An account with that phone number already exists'}), 404

    user_by_id = validate_user_by_id(data['idNumber'])
    if user_by_id:
        return jsonify({'error': 'An account with that ID number already exists'}), 404

    data['referee'] = referee
    data['accountType'] = account_type

    return create_cbn_user(data)

if __name__ == '__main__':
    # app.run()
    #https://fdf3-105-163-158-9.ngrok-free.app/callback,http://164.92.223.147:8081/callback,https://webhook.site/f5a9d5f9-eb2b-4823-afd1-c67ddc1bd498
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8081)), debug=True)
