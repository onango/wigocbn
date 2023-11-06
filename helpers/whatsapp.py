import requests
import json

api_url = "https://api.1msg.io/359900/"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
}
token = "BhtPYVBC5Wnw5gLNptpD"

def send_message(message_body, recipient_phone, urlq="sendMessage"):
    url = f"{api_url}{urlq}?token={token}"

    request_body = {
        "body": message_body,
        "phone": recipient_phone
    }

    # Convert the request body to JSON
    json_body = json.dumps(request_body)

    response = requests.post(url, headers=headers, data=json_body)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

def send_template_message(template, phone, text, urlq="sendTemplate"):
    message_body = route_templates(template, phone, text)
    url = f"{api_url}{urlq}?token={token}"

    response = requests.post(url, headers=headers, json=message_body)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None


def route_templates(template, phone, text):
    if template == "home":
        template_base["home"]["phone"] = phone
        new_text = "Updated text content"
        template_base["home"]["params"][0]["parameters"][0]["text"] = text
        return template_base["home"]
    if template == "airtime_home":
        template_base["airtime_home"]["phone"] = phone
        return template_base["airtime_home"]
    else:
        pass

template_base = {
    "home": {
        "namespace": "a7a20654_7e59_4fd9_b1de_9b398e9d3300",
        "template": "wigopay_welcome",
        "language": {"policy": "deterministic", "code": "en"},
        "params": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "test"}
                ]
            }
        ]
    },
    "airtime_home": {
        "namespace": "a7a20654_7e59_4fd9_b1de_9b398e9d3300",
        "template": "wigopay_buy_airtime_home",
        "language": {"policy": "deterministic", "code": "en"},
    },
    "template_2": {
        "namespace": "another_namespace",
        "template": "another_template",
        "language": {"policy": "deterministic", "code": "en_US"},
        "params": [
            {
                "type": "header",
                "parameters": [
                    {
                        "type": "image",
                        "image": {"link": "https://example.com/logo.png"}
                    }
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "another_test"}
                ]
            }
        ]
    }
}
