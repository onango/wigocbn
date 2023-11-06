import requests

def send_list_message(api_url, headers, token, message_body):
    # Define the URL
    url = f"{api_url}?token={token}"

    # Make the POST request with the provided JSON message body
    response = requests.post(url, headers=headers, json=message_body)

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
api_url = "https://api.1msg.io/359900/sendList"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
}
token = "BhtPYVBC5Wnw5gLNptpD"

message_body = {
    "body": "Choose one of the options displayed below",
    "header": "Available Cash: Ksh. 311.22",
    "footer": "Total Purchased: Ksh. 100",
    "action": "Click to select...",
    "sections": [
        {
            "title": "Select an action",
            "rows": [
                {
                    "id": "1",
                    "title": "Buy Airtime",
                    "description": "Description 1"
                },
                {
                    "id": "2",
                    "title": "Withdraw Cash",
                    "description": "Description 1"
                },
                {
                    "id": "3",
                    "title": "Invite new member",
                    "description": "Description 1"
                },
                {
                    "id": "4",
                    "title": "My Account",
                    "description": "Description 1"
                },
                {
                    "id": "5",
                    "title": "I need help",
                    "description": "Description 1"
                },
                {
                    "id": "6",
                    "title": "Registration Promotion",
                    "description": "Registration Promotion"
                }
            ]
        }
    ],
    "phone": 254721429815
}

response_data = send_list_message(api_url, headers, token, message_body)
if response_data:
    print(response_data)
