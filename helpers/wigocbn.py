import os
import json
import numpy as np
import datetime
from .db import connection
import random
import re
from datetime import datetime
from flask import jsonify
from helpers.whatsapp import *

def get_user_by_phone(phone):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM cbnUsers
        WHERE phone = %s
    """
    cursor.execute(select_query, (phone,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def whatsapp_history_log(phone, text):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)

    # Check if a record with the provided phone number exists
    select_query = """
        SELECT *
        FROM whatsapp_history_log
        WHERE phone = %s
    """
    cursor.execute(select_query, (phone,))
    existing_record = cursor.fetchone()

    if existing_record:
        prev_text = existing_record["text"]
        # Update the existing record
        update_query = """
            UPDATE whatsapp_history_log
            SET prev_text = %s, text = %s
            WHERE phone = %s
        """
        cursor.execute(update_query, (prev_text, text, phone))
    else:
        # Insert a new record
        insert_query = """
            INSERT INTO whatsapp_history_log (phone, text)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (phone, text))

    # Commit the changes
    cnx.commit()

    # Fetch and return the updated or inserted record
    cursor.execute(select_query, (phone,))
    result = cursor.fetchone()

    # Clean up
    cursor.close()
    cnx.close()

    return result


def whatsapp_history_log_next(phone, update_data):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)

    select_query = "SELECT * FROM whatsapp_history_log WHERE phone = %s"
    cursor.execute(select_query, (phone,))
    existing_json_data = cursor.fetchone()

    if existing_json_data:
        if 'next' in existing_json_data and existing_json_data['next'] is not None:
            existing_data_dict = json.loads(existing_json_data['next'])
        else:
            existing_data_dict = {}
    else:
        existing_data_dict = {}

    existing_data_dict.update(update_data)
    updated_json_data = json.dumps(existing_data_dict)

    if existing_json_data:
        update_query = "UPDATE whatsapp_history_log SET next = %s WHERE phone = %s"
    else:
        update_query = "INSERT INTO whatsapp_history_log (phone, next) VALUES (%s, %s)"

    cursor.execute(update_query, (updated_json_data, phone))
    cnx.commit()

    cursor.close()
    cnx.close()

def whatsapp_history_log_action(phone):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM whatsapp_history_log
        WHERE phone = %s
    """
    cursor.execute(select_query, (phone,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    print(result)
    if 'next' in result and result['next'] is not None:
        return json.loads(result['next'])
    else:
        return False

def generate_customer_code():
    while True:
        letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
        digits = str(random.randint(0, 999)).zfill(3)
        code = letters + digits
        if not user_exists_by_customer_code(code):
            return code

def generate_unique_id_cbn():
    while True:
        code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        remove_special_characters = re.sub('[^a-zA-Z0-9]', '', code)
        remove_characters = remove_special_characters.replace('Q', '').replace('I', '').replace('O', '').replace('0', '').replace('1', '')
        unique_code = remove_characters.upper()
        if not user_exists_by_referral_code(unique_code):
            return unique_code

def user_exists_by_customer_code(code):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM cbnUsers
        WHERE customerCode = %s
    """
    cursor.execute(select_query, (code,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def user_exists_by_referral_code(code):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM cbnUsers
        WHERE referralCode = %s
    """
    cursor.execute(select_query, (code,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def create_cbn_wallet(user_id):
    data = {
        'userID': user_id,
        'balance': 0.0,
        'update_at': datetime.now()
    }
    
    user = get_user_by_id(user_id)
    if user:
        return insert_cbn_wallet(data)

    return False

def get_user_by_id(user_id):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM cbnUsers
        WHERE userID = %s
    """
    cursor.execute(select_query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def insert_cbn_wallet(data):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    insert_query = """
        INSERT INTO cbnWallet (userID, balance, update_at)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (data['userID'], data['balance'], data['update_at']))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True

def create_cbn_user(data):
    phone = data['phone']
    referee = data['referee']
    is_free_registration = data['free_registration']
    code = generate_unique_id_cbn()

    user_data = {
        'phone': phone,
        'customerCode': generate_customer_code(),
        'referralCode': code,
        'initialType': 0 if is_free_registration else data['accountType'],
    }

    user_id = insert_cbn_user(user_data)

    if user_id:
        create_cbn_wallet(user_id)
        if referee:
            insert_cbn_referral(referee['userID'], user_id, referee['referralCode'])
        send_cbn_registration_sms(phone, code)

        return jsonify({
            'message': 'User created successfully',
            'customer_code': '1',
            'success': True,
        })

    return jsonify({'error': 'Failed to create user'}), 500

def insert_cbn_user(user_data):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    insert_query = """
        INSERT INTO cbnUsers (phone, customerCode, referralCode, initialType)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (user_data['phone'], user_data['customerCode'], user_data['referralCode'], user_data['initialType']))
    cnx.commit()
    user_id = cursor.lastrowid
    cursor.close()
    cnx.close()
    return user_id

def insert_cbn_referral(referee_id, user_id, referral_code):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    insert_query = """
        INSERT INTO cbnReferrals (refereeID, userID, referralCode)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (referee_id, user_id, referral_code))
    cnx.commit()
    cursor.close()
    cnx.close()

def send_cbn_registration_sms(phone, invite_code):
    message = f"You have successfully registered to wiGO Pay Airtime Network. WhatsApp #0702918033 to buy and earn. Your invite code is {invite_code}."
    # Replace this with your actual SMS sending code
    send_message(message, phone, urlq="sendMessage")
    print(f"Sending SMS to {phone}: {message}")

def validate_account_type(plan_type):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM accountType
        WHERE name = %s
    """
    cursor.execute(select_query, (plan_type,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def validate_referral(referral_code):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM cbnUsers
        WHERE referralCode = %s
    """
    cursor.execute(select_query, (referral_code,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def validate_user_by_phone(phone):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM cbnUsers
        WHERE phone = %s
    """
    cursor.execute(select_query, (phone,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def validate_user_by_id(id_number):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM cbnUsers
        WHERE idno = %s
    """
    cursor.execute(select_query, (id_number,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result

def get_user_wallet(id):
    cnx = connection()
    cursor = cnx.cursor(dictionary=True)
    select_query = """
        SELECT *
        FROM cbnWallet
        WHERE userID = %s
    """
    cursor.execute(select_query, (id,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result


print(get_user_by_phone("+254701515491"))
