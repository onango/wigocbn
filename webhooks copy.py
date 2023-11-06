from helpers.wigocbn import *
from helpers.whatsapp import *

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

    action = whatsapp_history_log_action(phone)

    log = {
    "text": "",
    "prev_text": ""
    }
    if msg_type == 0:
        log = whatsapp_history_log(phone, body)

    if body == "Join wigoPay Network":
        whatsapp_history_log_next(phone, {"action": "Join", "param": ""})
        message_body = "Thank you for your interest, please try again later!"
        send_message(message_body, phone, urlq="sendMessage")
    elif body == "Buy Airtime":
        whatsapp_history_log_next(phone, {"action": "BuyAirtime", "from": phone})
        send_template_message("airtime_home", phone, sender_name, urlq="sendTemplate")
    elif body == 'My Number':
        whatsapp_history_log_next(phone, {"action": "BuyAirtime", "from": phone})
        message_body = "Amount to recharge (Minimum Ksh. 10)"
        send_message(message_body, phone, urlq="sendMessage")

    elif body == "I need Help":
        whatsapp_history_log_next(phone, {"action": "Help", "param": ""})
        message_body = "How may I be of assistance?"
        send_message(message_body, phone, urlq="sendMessage")
    elif log['text'] == 'My Number':
        message_body = "Amount to recharge (Minimum Ksh. 10)"
        send_message(message_body, phone, urlq="sendMessage")
    elif log['prev_text'] == 'My Number':
        #recharge and send thanks
        # message_body = "Amount to recharge (Minimum Ksh. 10)"
        # send_message(message_body, phone, urlq="sendMessage")
        pass
    elif log['text'] == 'Other Number':
        message_body = "Please input the number to recharge. (Format 254XXXXXXXXX)"
        send_message(message_body, phone, urlq="sendMessage")
    elif log['prev_text'] == 'Other Number':
        whatsapp_history_log_next(phone, {"action": "BuyAirtime", "param": ""})
        message_body = "Amount to recharge (Minimum Ksh. 10)"
        send_message(message_body, phone, urlq="sendMessage")
        print('recharge no--')
        #recharge and send thanks
    elif log['text'] == 'Ask Amount':
        message_body = "Amount to recharge (Minimum Ksh. 10)"
        send_message(message_body, phone, urlq="sendMessage")
    elif log['text'] == 'Recharge':
        pass
        #recharge and send thanks
    elif log['text'] == 'I need Help':
        #send thanks template and return home
        pass
    else:
        if user and msg_type == 0:
            send_template_message("home", phone, sender_name, urlq="sendTemplate")
#send_template_message("home", "254701515491", "Antony", urlq="sendTemplate")
"webhookUrl": [
    "https://whatsapp.wigopay.com",
    "https://app.1msg.io/service/service_core/whatsapp/webhook/1949"
  ],

  "https://whatsapp.wigopay.com",
    "https://app.1msg.io/service/service_core/whatsapp/webhook/1949"
  ],