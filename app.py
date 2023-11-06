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

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8081)), debug=True)
