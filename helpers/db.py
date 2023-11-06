import mysql.connector


def connection():
    conn =  mysql.connector.connect(
        host="167.99.248.146",
        user="wigo_wallet",
        password="[aFM$D](tDt{",
        database="cbn_wallet"
    )
    return conn


# def fetch_visa(id):
#     cnx = establish_db_connection()
#     cursor = cnx.cursor(dictionary=True)
#     select_query = """
#         SELECT visa.*, img_encoding.path
#         FROM visa
#         LEFT JOIN img_encoding ON visa.id = img_encoding.user_id
#         WHERE visa.id = %s
#     """
#     cursor.execute(select_query, (id,))
#     result = cursor.fetchall()
#     cursor.close()
#     cnx.close()
#     return result[0]


# def insert(pathList):
#     cnx = establish_db_connection()
#     # Establish a connection to the MySQL database

#     # Insert the encoding value into the database
#     cursor = cnx.cursor()
#     insert_query = "INSERT INTO profiles (path, encoding) VALUES (%s, %s)"
#     cursor.execute(insert_query, (path, encoding))
#     cnx.commit()
#     # Close the cursor and connection
#     cursor.close()
#     cnx.close()


# def fetch_all():
#     cnx = establish_db_connection()
#     cursor = cnx.cursor()
#     select_query = "SELECT encoding, user_id FROM img_encoding"
#     cursor.execute(select_query)
#     result = cursor.fetchall()  # Assuming a single result
#     # Parse the JSON string
#     # json_array = json.loads(result)

#     # # Convert the JSON array back to a NumPy array
#     # numpy_array = np.array(json_array)

#     # Close the cursor and connection
#     cursor.close()
#     cnx.close()
#     encodedList = []
#     user_ids = []
#     for r in result:
#         encodedList.append(np.array(json.loads(r[0])))
#         user_ids.append(r[1])

#     return encodedList, user_ids


# def fetch_visa(id):
#     cnx = establish_db_connection()
#     cursor = cnx.cursor(dictionary=True)
#     select_query = """
#         SELECT visa.*, img_encoding.path
#         FROM visa
#         LEFT JOIN img_encoding ON visa.id = img_encoding.user_id
#         WHERE visa.id = %s
#     """
#     cursor.execute(select_query, (id,))
#     result = cursor.fetchall()
#     cursor.close()
#     cnx.close()
#     return result[0]


# def findEncodings(imagesList):
#     encodeList = []
#     for img in imagesList:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)

#     return encodeList


# def insert_visa(folderPath, path, data):
#     encoding = json.dumps(img_encode(folderPath, path).tolist())

#     cnx = establish_db_connection()
#     cursor = cnx.cursor()
#     insert_query = "INSERT INTO visa (full_name, fname, lname, contact, passport, email, country, residence, profession, visa_type, purpose, travel_date) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

#     values = (
#         data['fname'] + ' ' + data['lname'],
#         data['fname'],
#         data['lname'],
#         data['contact'],
#         data['passport'],
#         data['email'],
#         data['country'],
#         data['residence'],
#         data['profession'],
#         data['visa_type'],
#         data['purpose'],
#         data['travel_date']
#     )

#     cursor.execute(insert_query, values)
#     cnx.commit()
#     last_insert_id = cursor.lastrowid
#     # Close the cursor and connection
#     cursor.close()
#     # cnx.close()

#     # Insert the encoding value into the database
#     cursor = cnx.cursor()
#     insert_query = "INSERT INTO img_encoding (path, encoding, user_id) VALUES (%s, %s, %s)"
#     cursor.execute(insert_query, (path, encoding, last_insert_id))
#     cnx.commit()
#     # Close the cursor and connection
#     cursor.close()
#     cnx.close()

# def insert_check(data):
#     cnx = establish_db_connection()
#     cursor = cnx.cursor()

#     # Check if a matching visa clearance already exists for the user ID
#     select_query = "SELECT * FROM visa_clearance WHERE user_id = %s ORDER BY created_at DESC LIMIT 1"
#     cursor.execute(select_query, (data['user_id'],))
#     result = cursor.fetchone()

#     if result is None:
#         # No existing clearance found, insert a new one
#         insert_query = "INSERT INTO visa_clearance (user_id) VALUES (%s)"
#         values = (data['user_id'],)
#         cursor.execute(insert_query, values)
#         cnx.commit()
#         last_insert_id = cursor.lastrowid
#         print("New visa clearance inserted.")
#     else:
#         # Check if the most recent clearance was created within the last two minutes
#         created_at = result[2]  # Assuming created_at column is at index 2
#         current_time = datetime.datetime.now()
#         time_diff = current_time - created_at

#         if time_diff.total_seconds() > 120:
#             # Insert a new clearance if the last one was created more than two minutes ago
#             insert_query = "INSERT INTO visa_clearance (user_id) VALUES (%s)"
#             values = (data['user_id'],)
#             cursor.execute(insert_query, values)
#             cnx.commit()
#             last_insert_id = cursor.lastrowid
#             print("New visa clearance inserted.")
#         else:
#             # Do nothing if the last clearance was created within the last two minutes
#             print("No action needed. Recent visa clearance exists.")

#     # Close the cursor and connection
#     cursor.close()
#     cnx.close()
