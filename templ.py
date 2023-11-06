import requests

def send_template_message(api_url, headers, token, message_body):
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
api_url = "https://api.1msg.io/359900/sendTemplate"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
}
token = "BhtPYVBC5Wnw5gLNptpD"

message_body = {
    "namespace": "a7a20654_7e59_4fd9_b1de_9b398e9d3300",
    "template": "sample_purchase_feedback",
    "language": { "policy":"deterministic", "code":"en_US"},
    "phone": 254701515491,
    "params":[{"type":"header","parameters":[{"type":"image","image": {"link":"https://account.intrepid.co.ke/assets/media/image/logo-bg.png"}}]},{"type":"body","parameters":[{"type":"text","text":"test"}]}]
    
}

response_data = send_template_message(api_url, headers, token, message_body)
if response_data:
    print(response_data)
