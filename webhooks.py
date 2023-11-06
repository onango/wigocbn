from helpers.wigocbn import *
from helpers.whatsapp import *
import requests

cache = {}

def handle_callback(callback_event):
    # Check the type of the callback event
    instance_id = callback_event.get('instanceId')

    if 'messages' in callback_event:
        messages = callback_event.get('messages', [])
        for message in messages:
            handle_message(message)

    if 'ack' in callback_event:
        acknowledgments = callback_event.get('ack', [])
        for ack in acknowledgments:
            handle_acknowledgment(ack)

    print(f"Instance ID: {instance_id}")

def handle_message(message):
    id = message.get('id')
    body = message.get('body')
    sender_name = message.get('senderName')

    check_user(message)
    # "fromMe": false,
    #   "self": 0

    print(f"Received message with id {id} from {sender_name}: {body}")

def handle_acknowledgment(ack):
    ack_id = ack.get('id')
    chat_id = ack.get('chatId')
    status = ack.get('status')
    # Add your custom logic to handle the acknowledgment here
    print(f"Acknowledgment received for message ID {ack_id} in chat {chat_id}. Status: {status}")


def check_user(message):
    msg_init = message.get('fromMe') #false
    msg_type = message.get('self') #0
    sender_name = message.get('senderName')
    phone = message.get('chatName')
    user = get_user_by_phone("+" + phone)
    body = message.get('body')

    if msg_type == 0:
        store_data(phone, "action", body)

    action = read_data(phone, "action")
    next_action = read_data(phone, "next_action")

    if msg_type == 0 and action == "Join wigoPay Network":
        whatsapp_history_log_next(phone, {"action": "Join", "param": ""})
        message_body = "Thank you for your interest, please try again later!"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'help_ack':
        update_data(phone, "next_action", "")
        message_body = "Thank you for your enquiry!"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and action == "I need Help":
        update_data(phone, "next_action", "help_ack")
        message_body = "Please leave a message"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and action == "Buy Airtime":
        update_data(phone, "airtime_from", phone)
        send_template_message("airtime_home", phone, sender_name, urlq="sendTemplate")
    elif msg_type == 0 and action == "My Number":
        update_data(phone, "recipient", phone)
        update_data(phone, "next_action", "recharge")
        message_body = "Amount to recharge (Minimum Ksh. 10)"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and action == "Other Number":
        update_data(phone, "next_action", "askAmountOther")
        message_body = "Enter Phone Number (254XXXXXXXXX)"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'askAmountOther':
        update_data(phone, "recipient", action)
        update_data(phone, "next_action", "recharge")
        message_body = "Amount to recharge (Minimum Ksh. 10)"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'recharge':
        #purchase and delete the action
        update_data(phone, "next_action", "")
        #message_body = "Thanks for the order of "+action+" "+phone+" "+read_data(phone, "recipient")
        message_body = "Thanks, Your airtime request is being processed"
        send_message(message_body, phone, urlq="sendMessage")
        make_stkpush_request(phone, read_data(phone, "recipient"), action)
   
    # elif action['action'] == 'Recharge':
    #     pass

    else:
        if user and msg_type == 0:
            send_template_message("home", phone, sender_name, urlq="sendTemplate")
#send_template_message("home", "254701515491", "Antony", urlq="sendTemplate")
# phone = "254701515491"
# whatsapp_history_log_next(phone, {"action": "BuyAirtime1", "airtime_from": phone})


# Function to store data in the cache
def store_data(key, sub_key, value):
    if key in cache:
        cache[key][sub_key] = value
    else:
        cache[key] = {sub_key: value}

# Function to read data from the cache
def read_data(key, sub_key):
    if key in cache:
        return cache[key].get(sub_key, None)
    else:
        return None

# Function to update data in the cache
def update_data(key, sub_key, new_value):
    if key in cache:
        cache[key][sub_key] = new_value
    else:
        cache[key] = {sub_key: new_value}


# Store data in the cache
# store_data("a", "name", 1)
# store_data("b", "city", "New York")

# # Read and print data from the cache
# name = read_data("a", "name")
# print(f"Name: {name}")

# city = read_data("b", "city")
# print(f"City: {city}")

# # Update data in the cache
# update_data("b", "city", "Los Angeles")

# # Read and print updated data from the cache
# updated_city = read_data("b", "city")
# print(f"Updated City: {updated_city}")




def make_stkpush_request(phone, recipient, amount):
    # Define the URL for the POST request
    url = 'https://account.intrepid.co.ke/api/v1/wigocbn/stkpush'

    # Define the data to send in the request
    data = {
        'phone': "+"+phone,
        'recipients': "+"+recipient,
        'amount': amount
    }

    try:
        # Make the POST request
        response = requests.post(url, data=data)

        # Check the response status code
        if response.status_code == 200:
            print("Request was successful")
            # You can access the response content if needed
            print(response.text)
        else:
            print("Request failed with status code:", response.status_code)
            print(response.text)
            message_body = "Sorry, airtime request failed, please contact support"
            # send_message(message_body, phone, urlq="sendMessage")
    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e))
        message_body = "Sorry, airtime request failed, please contact support"
        # send_message(message_body, phone, urlq="sendMessage")

# Example usage:
# make_stkpush_request('254701515491', '+254701515491', 10)
