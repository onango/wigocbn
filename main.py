import requests

def get_me(api_url, headers, token):
    # Define the URL
    url = f"{api_url}?token={token}"

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        # Request was successful
        data = response.json()  # If the response is in JSON format
        return data
    else:
        # Request was not successful, handle the error
        print(f"Request failed with status code {response.status_code}")
        print(response.text)  # Print the response content for debugging
        return None

import requests
import json

def send_message(api_url, headers, token, message_body, recipient_phone):
    # Define the URL
    url = f"{api_url}?token={token}"

    # Define the request body as a Python dictionary
    request_body = {
        "body": message_body,
        "phone": recipient_phone
    }

    # Convert the request body to JSON
    json_body = json.dumps(request_body)

    # Make the POST request
    response = requests.post(url, headers=headers, data=json_body)

    # Check the response
    if response.status_code == 200:
        # Request was successful
        data = response.json()  # If the response is in JSON format
        return data
    else:
        # Request was not successful, handle the error
        print(f"Request failed with status code {response.status_code}")
        print(response.text)  # Print the response content for debugging
        return None

# Example usage
api_url = "https://api.1msg.io/359900/sendMessage"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
}
token = "BhtPYVBC5Wnw5gLNptpD"
message_body = "Hello"
recipient_phone = 254701515491

response_data = send_message(api_url, headers, token, message_body, recipient_phone)
if response_data:
    print(response_data)


# Example usage
api_url = "https://api.1msg.io/359900/me"
headers = {
    "accept": "application/json",
    "content-type": "text/plain",
}
token = "BhtPYVBC5Wnw5gLNptpD"

response_data = get_me(api_url, headers, token)
# if response_data:
#     print(response_data)


import requests
import json

def set_webhook(api_url, headers, token, webhook_url):
    # Define the URL
    url = f"{api_url}?token={token}"

    # Define the request body as a Python dictionary
    request_body = {
        "webhookUrl": webhook_url
    }

    # Convert the request body to JSON
    json_body = json.dumps(request_body)

    # Make the POST request
    response = requests.post(url, headers=headers, data=json_body)

    # Check the response
    if response.status_code == 200:
        # Request was successful
        data = response.json()  # If the response is in JSON format
        return data
    else:
        # Request was not successful, handle the error
        print(f"Request failed with status code {response.status_code}")
        print(response.text)  # Print the response content for debugging
        return None

# Example usage
api_url = "https://api.1msg.io/359900/webhook"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
}
token = "BhtPYVBC5Wnw5gLNptpD"
webhook_url = ["https://webhook.site/89734621-ee5c-4ac0-a64a-20c5d6663a76","https://d833-105-163-1-111.ngrok-free.app"]

# response_data = set_webhook(api_url, headers, token, webhook_url)
# if response_data:
#     print(response_data)


# "webhookUrl": [
#     "https://whatsapp.wigopay.com",
#     "https://app.1msg.io/service/service_core/whatsapp/webhook/1949"
#   ],
