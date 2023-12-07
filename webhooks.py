from helpers.wigocbn import *
from helpers.whatsapp import *
import requests
import json
from flask import jsonify

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
    list_reply = message.get('list_reply', {})
    list_reply_id = list_reply.get('id', '')

    if msg_type == 0:
        store_data(phone, "action", body)

    action = read_data(phone, "action")
    next_action = read_data(phone, "next_action")
    print("ACT ------------------",action, msg_type)

    if msg_type == 0 and action == "Withdraw Cash":
        update_data(phone, "next_action", "")
        update_data(phone, "action", "")
        message_body = "This feature is under maintenance, please check later! type *home* to return to main menu"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and action == "Join wigoPay Network":
        # print("ACT2 ------------------",action, msg_type)
        send_template_message("plan_type_home", phone, sender_name, urlq="sendTemplate")
    elif msg_type == 0 and action == "Free plan":
        update_data(phone, "plan_type", action)
        update_data(phone, "next_action", "id_no")
        message_body = "Enter your Invite code"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and action == "Paid plan":
        account_plans['phone'] = phone
        message_body = account_plans
        send_list_message(message_body, urlq="sendList")
    elif msg_type == 0 and next_action is not None and next_action == 'Join':
        send_template_message("plan_home", phone, sender_name, urlq="sendTemplate")
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'id_no':
        update_data(phone, "next_action", "next_kin")
        update_data(phone, "invite_code", action)
        message_body = "ID of Next of Kin"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'next_kin':
        update_data(phone, "next_action", "next_kin_no")
        update_data(phone, "id_no", action)
        message_body = "Name of next of Kin"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'next_kin_no':
        update_data(phone, "next_kin", action)
        update_data(phone, "next_action", "complete_join")
        message_body = "Phone Number of next of Kin"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'complete_join':
        update_data(phone, "next_kin_no", action)
        update_data(phone, "next_action", "")
        message_body = "Thank you, your request is being processed"
        send_message(message_body, phone, urlq="sendMessage")
        join_wigopay(phone)
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
    elif msg_type == 0 and action == "View More":
        my_account_list['phone'] = phone
        message_body = my_account_list
        send_list_message(message_body, urlq="sendList")
    # elif msg_type == 0 and action == "old pin":
    #     update_data(phone, "next_action", "confirm_current_pin")
    #     message_body = "Enter Current PIN"
    #     send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'confirm_current_pin':
        update_data(phone, "pin_current", action)
        if read_data(phone, "pin_current") == "0000":
            update_data(phone, "next_action", "confirm_pin")
            message_body = "Enter PIN  (4 digits)"
            send_message(message_body, phone, urlq="sendMessage")
        else:
            # update_data(phone, "next_action", "")
            message_body = "Current Pin not matched, Enter Current PIN"
            send_message(message_body, phone, urlq="sendMessage")
    # elif msg_type == 0 and action == "new pin":
    #     update_data(phone, "next_action", "confirm_pin")
    #     message_body = "Enter PIN  (4 digits)"
    #     send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'confirm_pin':
        update_data(phone, "pin", action)
        update_data(phone, "next_action", "set_pin")
        message_body = "Confirm PIN  (4 digits)"
        send_message(message_body, phone, urlq="sendMessage")
    elif msg_type == 0 and next_action is not None and next_action == 'set_pin':
        update_data(phone, "pin_confirmation", action)
        if read_data(phone, "pin") == read_data(phone, "pin_confirmation"):
            update_data(phone, "next_action", "")
            message_body = "Pin Match"
            send_message(message_body, phone, urlq="sendMessage")
        else:
            # update_data(phone, "next_action", "")
            message_body = "Pin not match, Confirm PIN  (4 digits)"
            send_message(message_body, phone, urlq="sendMessage")

    elif list_reply_id:
        if list_reply_id == "pin_change":
            user_info = get_user_by_phone("+"+phone)
            if user_info:
                user_pin = user_info['pin']
                if user_pin:
                    update_data(phone, "next_action", "confirm_current_pin")
                    message_body = "Enter Current PIN"
                    send_message(message_body, phone, urlq="sendMessage")
                else:
                    update_data(phone, "next_action", "confirm_pin")
                    message_body = "Enter PIN  (4 digits)"
                    send_message(message_body, phone, urlq="sendMessage")
            else:
                update_data(phone, "next_action", "confirm_pin")
                message_body = "Enter PIN  (4 digits)"
                send_message(message_body, phone, urlq="sendMessage")

        else:
            process_list_reply(list_reply_id, phone)
    elif msg_type == 0 and any(char.isalpha() or char.isdigit() for char in action):
        user_info = get_user_by_phone("+"+phone)
        if user_info:
            user_id = user_info['userID']
            wallet_balance = get_user_wallet(user_id)["balance"]
            header_text = f"Cash A/C: KES {wallet_balance}, Loan A/C: KES 0.00"
            send_template_message2("home_registered", phone, sender_name, header_text, urlq="sendTemplate")
        else:
            send_template_message("home", phone, sender_name, urlq="sendTemplate")
   
    # elif action['action'] == 'Recharge':
    #     pass

    # else:
    #     if user and msg_type == 0:
    #         send_template_message("home", phone, sender_name, urlq="sendTemplate")
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


def join_wigopay(phone):

    data = {
        'phone': "+"+phone,  
        'idNumber': read_data(phone, "id_no"),      
        'referralCode': read_data(phone, "invite_code"),
        'constituency': '',
        'nextKin': read_data(phone, "next_kin"),
        'nextKinNo': read_data(phone, "next_kin_no"),  
        'planType': read_data(phone, "plan_type"), 
    }

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

    user_data = {
        'phone': "+"+phone,  
        'idNumber': read_data(phone, "id_no"),      
        'referralCode': read_data(phone, "invite_code"),
        'constituency': '',
        'nextKin': read_data(phone, "next_kin"),
        'nextKinNo': read_data(phone, "next_kin_no"),  
        'planType': read_data(phone, "plan_type"), 
    }
    print('User Data', user_data)


    registration_url = 'https://account.intrepid.co.ke/api/v1/wigocbn/register-user'
    #'https://account.intrepid.co.ke/api/v1/wigocbn/register-user'

    # try:
    #     # Making a POST request
    #     response = requests.post(registration_url, json=user_data)

    #     # Check if the request was successful (status code 2xx)
    #     response.raise_for_status()

    #     # Print the response status code and content
    #     print('Response Status Code:', response.status_code)
    #     print('Response Content:', response.text)

    # except requests.exceptions.HTTPError as errh:
    #     print(f"HTTP Error: {errh}")
    # except requests.exceptions.ConnectionError as errc:
    #     print(f"Error Connecting: {errc}")
    # except requests.exceptions.Timeout as errt:
    #     print(f"Timeout Error: {errt}")
    # except requests.exceptions.RequestException as err:
    #     print(f"Request Exception: {err}")




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

account_plans = {
    "body": "Choose one of the options displayed below",
    "header": "Paid Premium membership plans",
    "footer": "",
    "action": "Click to select...",
    "sections": [
        {
            "title": "Select membership plan",
            "rows": [
                {
                    "id": "plan-1",
                    "title": "Basic Plan Ksh. 1500",
                    "description": "Basic Membership plan"
                },
                {
                    "id": "plan-2",
                    "title": "Silver Plan Ksh. 3000",
                    "description": "Silver Membersip plan"
                },
                {
                    "id": "plan-3",
                    "title": "Gold Plan Ksh. 5000",
                    "description": "Gold Membership plan"
                }
            ]
        }
    ],
    "phone": 254701515491
}

my_account_list = {
    "body": "Choose one of the options displayed below",
    "header": "My Account",
    "footer": "",
    "action": "Click to select...",
    "sections": [
        {
            "title": "Select ...",
            "rows": [
                {
                    "id": "pin_change",
                    "title": "Pin Change",
                    "description": "Change your Password"
                },
                {
                    "id": "txn_summary",
                    "title": "Transaction Summary",
                    "description": "A summary of airtime transactions"
                },
                {
                    "id": "mini_stmt",
                    "title": "Mini Statement",
                    "description": "Airtime transaction mini statements"
                },
                {
                    "id": "upgrade_plan",
                    "title": "Upgrade Plan",
                    "description": "Upgrade plan/membership"
                },
                {
                    "id": "my_network",
                    "title": "My Network",
                    "description": "Your network list"
                }
            ]
        }
    ],
    "phone": 254701515491
}

def format_statement(phone):
    result_string = ""
    user_info = get_user_by_phone("+"+phone)
    if user_info:
        user_id = user_info['userID']
        response_data = mini_statement(user_id)
        # Convert each item to one string variable
        result_string = "Prev Balance | Amount | New Balance | Description\n"

        # Convert each item to one string variable
        for item in response_data:
            result_string += (
                f"{item['prev_balance']} | {item['amount']} | {item['new_balance']} | {item['description']}\n"
            )
        return result_string

def process_list_reply(list_reply_id, phone):
    
    if list_reply_id == "txn_summary":
        message_body = format_statement(phone)
        send_message(message_body, phone, urlq="sendMessage")
        # Additional code for Transaction Summary

    elif list_reply_id == "mini_stmt":
        message_body = format_statement(phone)
        send_message(message_body, phone, urlq="sendMessage")
        # Additional code for Mini Statement

    # elif list_reply_id == "upgrade_plan":
    #     print("Processing Upgrade Plan:")
    #     print("Title:", list_reply.get('title', ''))
    #     print("Description:", list_reply.get('description', ''))
    #     # Additional code for Upgrade Plan

    # elif list_reply_id == "my_network":
    #     print("Processing My Network:")
    #     print("Title:", list_reply.get('title', ''))
    #     print("Description:", list_reply.get('description', ''))
        # Additional code for My Network

    else:
        message_body = "This feature is under maintenance, please check later! type *home* to return to main menu"
        send_message(message_body, phone, urlq="sendMessage")

        