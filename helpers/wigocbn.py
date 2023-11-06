import os
import json
import numpy as np
import datetime
from helpers.db import connection


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


